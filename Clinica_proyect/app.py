from flask import Flask, request, render_template
from flask_cors import CORS
from controller.database import initialize_database
from controller.models import *  # agregar todos los modelos
import sqlite3
import random

app = Flask(__name__)
CORS(app)

initialize_database()
print("Database initialized")


# Ruta principal (página de inicio)
@app.route("/")
def index():
    # Mostrar un menú de opciones para el usuario
    return render_template("user/login.html")


@app.route("/cargar_horario", methods=["GET"])
def horario():
    return render_template("user/cargar_horario.html")


@app.route("/crear_citas", methods=["GET"])
def crear_citas():
    return render_template("user/crear_citas.html")


@app.route("/registro/paciente")
def registro_paciente():
    return render_template("user/registro_paciente.html")


@app.route("/registro/doctor")
def registro_doctor():
    return render_template("user/registro_doctor.html")


@app.route("/tipo_usuario")
def perfil():
    return render_template("user/tipo_usuario.html")

@app.route("/ver_citas")
def ver_cita():
    return render_template("user/ver_citas.html")


@app.route("/menulateral", methods=["GET"])
def menulateral():
    return render_template("user/menulateral.html")

@app.route("/disponibilidad_horarios", methods=["GET"])
def disponibilidad_horarios():
    return render_template("user/disponibilidad_horarios.html")


@app.route("/contacto", methods=["GET"])
def contacto():
    return render_template("user/contacto.html")


@app.route("/paciente/<int:id>", methods=["GET"])
def obtener_paciente(id):
    try:
        paciente = Paciente.find_by_id(id)
        pacienteJson = {
            "id": paciente[0],
            "name": paciente[2],
            "identificacion_tipo": paciente[3],
            "identificacion_numero": paciente[4],
            "telefono": paciente[5],
            "direccion": paciente[6],
            "descendencia": paciente[7],
            "nombre_hijo": paciente[8],
            "fecha_nacimiento_hijo": paciente[9],
            "sexo_hijo": paciente[10],
            "fecha_nacimiento": paciente[11],
            "sexo": paciente[12],
            "patologia": paciente[13],
        }
        if not paciente:
            return {"error": "Paciente no encontrado"}, 404
        return {"paciente": pacienteJson}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/doctores", methods=["GET"])
def doctores():
    doctores = Doctor.list()
    return {"doctores": doctores}, 200


@app.route("/doctor/<int:id>", methods=["GET"])
def obtener_doctor(id):
    try:
        doctor = Doctor.find_by_id(id)
        horarios = HorariosDoctor.get_by_doctor_id(id)
        doctorJson = {
            "id": doctor[0],
            "nombre": doctor[1],
            "nacimiento": doctor[2],
            "sexo": doctor[3],
            "cedula": doctor[4],
            "carnet": doctor[5],
            "especialidades": doctor[6],
            "horarios": horarios,
        }
        if not doctor:
            return {"error": "Doctor no encontrado"}, 404
        return {"doctor": doctorJson}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/historial/<int:id>", methods=["GET"])
def obtener_historial(id):
    try:
        historial = HistorialCitas.list_by_patient(id)
        if not historial:
            return {"error": "Historial no encontrado"}, 404
        return {"historial": historial}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/registro_doctor", methods=["POST"])
def doctor():
    try:
        data = request.get_json()
        nombre = data["nombre"]
        nacimiento = data["nacimiento"]
        sexo = data["sexo"]
        cedula = data["cedula"]
        carnet = generar_nro_carnet()
        especialidades = [data["especialidad"]]
        clave = data["clave"]
        confirmar_clave = data["confirmar_clave"]

        if clave != confirmar_clave:
            return {"error": "Las claves no coinciden"}, 400

        doctor = Doctor(nombre, nacimiento, sexo, cedula, carnet, especialidades, clave)
        doctor.save()
        return {"message": "Doctor creado exitosamente"}, 201
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/registro_paciente", methods=["POST"])
def paciente():
    try:
        data = request.get_json()
        name = data["name"]
        identificacion_tipo = data["identificacion_tipo"]
        identificacion_numero = data["identificacion_numero"]
        telefono = data["telefono"]
        direccion = data["direccion"]
        descendencia = data["descendencia"]
        nombre_hijo = data["nombre_hijo"]
        fecha_nacimiento_hijo = data["fecha_nacimiento_hijo"]
        sexo_hijo = data["sexo_hijo"]
        fecha_nacimiento = data["fecha_nacimiento"]
        sexo = data["sexo"]
        patologia = data["patologia"]
        usuario = data["usuario"]
        clave = data["clave"]
        confirmar_clave = data["confirmar_clave"]

        if clave != confirmar_clave:
            return {"error": "Las claves no coinciden"}, 400
        user = User(username=usuario, password=clave, role="paciente")
        user.save()
        id = User.find_id_by_username(usuario)

        paciente = Paciente(
            name=name,
            user_id=id,
            identificacion_tipo=identificacion_tipo,
            identificacion_numero=identificacion_numero,
            telefono=telefono,
            direccion=direccion,
            descendencia=descendencia,
            nombre_hijo=nombre_hijo,
            fecha_nacimiento_hijo=fecha_nacimiento_hijo,
            sexo_hijo=sexo_hijo,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            patologia=patologia,
        )
        paciente.save()
        return {"message": "Paciente creado exitosamente"}, 201
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/menu")
def menu_lateral():
    return render_template("user/menulateral.html")


@app.route("/citas", methods=["GET"])
def citas():
    return render_template("user/ver_citas.html")


@app.route("/crear_cita", methods=["POST"])
def crear_cita_route():
    try:
        data = request.get_json()
        doctor_id = data["doctor_id"]
        patient_id = data["patient_id"]
        fecha = data["fecha"]
        motivo = data["motivo"]

        # Validar que el doctor exista
        doctor = Doctor.find_by_id(doctor_id)
        if not doctor:
            return {"error": "El doctor no existe"}, 404

        # Validar que el paciente exista
        patient = Paciente.find_by_identificacion_numero(patient_id)
        if not patient:
            return {"error": "El paciente no existe"}, 404

        cita = Cita(doctor_id, patient_id, fecha, motivo)
        cita.save()

        return {"message": "Cita creada exitosamente"}, 201
    except KeyError as e:
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        user = User.find_by_username(username)
        if user is None or not user.check_password(password):
            return {"error": "Usuario o clave incorrecta"}, 401
        print(user.role)
        print(user.id_paciente)
        print(user.id_doctor)
        if user.role == "paciente":
            id = user.id_paciente
        else:
            id = user.id_doctor
        return {"message": "Inicio de sesión exitoso", "id": id, "role": user.role}, 200
    except KeyError as e:
        return {"error": f"Falta el campo requerido: {str(e)}"}, 400
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/citas/listar/<int:doctor_id>", methods=["GET"])
def list_citas(doctor_id):
    try:
        citas = Cita.list_by_doctor(
            doctor_id
        )  # Ensure Cita has a method to list by doctor_id
        return {"citas": citas}, 200
    except Exception as e:
        return {"error": str(e)}, 500


def generar_nro_carnet():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        while True:
            nro_carnet = str(random.randint(100000, 999999))
            cursor.execute(
                "SELECT nro_carnet FROM doctores WHERE nro_carnet = ?", (nro_carnet,)
            )
            if not cursor.fetchone():
                return nro_carnet


if __name__ == "__main__":
    app.run(debug=True)
