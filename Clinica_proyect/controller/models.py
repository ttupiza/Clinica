import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


class Doctor:
    def __init__(self, nombre, nacimiento, sexo, cedula, carnet, especialidades, clave):
        self.nombre = nombre
        self.nacimiento = nacimiento
        self.sexo = sexo
        self.cedula = cedula
        self.carnet = carnet
        self.especialidades = especialidades
        self.clave = generate_password_hash(clave)

    def save(self):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO doctores (nombre, fecha_nacimiento, sexo, cedula, nro_carnet, clave, especialidad)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        self.nombre,
                        self.nacimiento,
                        self.sexo,
                        self.cedula,
                        self.carnet,
                        self.clave,
                        self.especialidades[0],
                    ),
                )
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error de SQLite: {e}")
                raise e

    def list():
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM doctores")
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "nombre": row[1],
                    "fecha_nacimiento": row[2],
                    "sexo": row[3],
                    "cedula": row[4],
                    "nro_carnet": row[5],
                    "especialidad": row[7],
                }
                for row in rows
            ]

    def find_by_id(doctor_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM doctores WHERE id = ?", (doctor_id,))
            return cursor.fetchone()


class Cita:
    def __init__(self, doctor_id, patient_id, fecha, atendida, motivo):
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.fecha = fecha
        self.motivo = motivo
        self.atendida = atendida

    def save(self):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO citas (doctor_id, patient_id, fecha, atendida,  motivo)
                VALUES (?, ?, ?, ?)
            """,
                (
                    self.doctor_id,
                    self.patient_id,
                    self.fecha,
                    self.atendida,
                    self.motivo,
                ),
            )
            conn.commit()

    def mark_as_attended(appointment_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE citas SET atendida = 1 WHERE id = ?", (appointment_id,)
            )
            conn.commit()

    @staticmethod
    def find_by_id(appointment_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
            return cursor.fetchone()

    @staticmethod
    def list_by_doctor(doctor_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 
                    citas.id, 
                    citas.patient_id,
                    citas.doctor_id,
                    doctores.nombre AS doctor_nombre, 
                    patients.name AS paciente_nombre, 
                    citas.fecha, 
                    citas.motivo
                FROM citas
                JOIN doctores ON citas.doctor_id = doctores.id
                JOIN patients ON citas.patient_id = patients.id
                WHERE citas.atendida = 0
                AND citas.doctor_id = ?
                """,
                (doctor_id,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "patient_id": row[1],
                    "doctor_id": row[2],
                    "doctor_nombre": row[3],
                    "paciente_nombre": row[4],
                    "fecha": row[5],
                    "motivo": row[6],
                }
                for row in rows
            ]


class Paciente:  # Ensure Paciente is imported and used here
    def __init__(
        self,
        user_id,
        name,
        identificacion_tipo,
        identificacion_numero,
        telefono,
        direccion,
        descendencia,
        nombre_hijo,
        fecha_nacimiento_hijo,
        sexo_hijo,
        fecha_nacimiento,
        sexo,
        patologia,
    ):
        self.user_id = user_id
        self.name = name
        self.identificacion_tipo = identificacion_tipo
        self.identificacion_numero = identificacion_numero
        self.telefono = telefono
        self.direccion = direccion
        self.descendencia = descendencia
        self.nombre_hijo = nombre_hijo
        self.fecha_nacimiento_hijo = fecha_nacimiento_hijo
        self.sexo_hijo = sexo_hijo
        self.fecha_nacimiento = fecha_nacimiento
        self.sexo = sexo
        self.patologia = patologia

    def save(self):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO patients (user_id, name, identificacion_tipo, identificacion_numero, telefono, direccion, descendencia, nombre_hijo, fecha_nacimiento_hijo, sexo_hijo, fecha_nacimiento, sexo, patologia)
                VALUES (?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?)
            """,
                (
                    self.user_id,
                    self.name,
                    self.identificacion_tipo,
                    self.identificacion_numero,
                    self.telefono,
                    self.direccion,
                    self.descendencia,
                    self.nombre_hijo,
                    self.fecha_nacimiento_hijo,
                    self.sexo_hijo,
                    self.fecha_nacimiento,
                    self.sexo,
                    self.patologia,
                ),
            )
            conn.commit()

    def find_by_id(patient_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
            return cursor.fetchone()

    def find_by_identificacion_numero(identificacion_numero):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM patients WHERE identificacion_numero = ?",
                (identificacion_numero,),
            )
            return cursor.fetchone()


class User:
    def __init__(self, username, password, id_paciente, id_doctor, role):
        self.username = username
        self.role = role
        self.password = password
        self.id_paciente = id_paciente
        self.id_doctor = id_doctor

    def save(self):
        hash_password = generate_password_hash(self.password)
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (username, password, role, id_paciente, id_doctor)
                VALUES (?, ?, ?)
            """,
                (
                    self.username,
                    hash_password,
                    self.role,
                    self.id_paciente,
                    self.id_doctor,
                ),
            )
            conn.commit()

    @staticmethod
    def find_by_username(username):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return User(
                    username=row[1],
                    password=row[2],
                    id_doctor=row[3],
                    id_paciente=row[4],
                    role=row[5],
                )
            return None

    def find_id_by_username(username):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return row[0]
            return None

    def check_password(self, password):
        return check_password_hash(self.password, password)


class HorariosDoctor:
    def __init__(self, doctor_id, dia, hora_inicio, hora_fin):
        self.doctor_id = doctor_id
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

    def save(self):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO horarios_doctor (doctor_id, dia, hora_inicio, hora_fin)
                VALUES (?, ?, ?, ?)
            """,
                (self.doctor_id, self.dia, self.hora_inicio, self.hora_fin),
            )
            conn.commit()

    @staticmethod
    def get_by_doctor_id(doctor_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT dia, hora_inicio, hora_fin FROM horarios_doctor WHERE doctor_id = ?",
                (doctor_id,),
            )
            rows = cursor.fetchall()
            return [
                {"dia": row[0], "hora_inicio": row[1], "hora_fin": row[2]}
                for row in rows
            ]


class HistorialCitas:
    def __init__(self, id_doctor, id_paciente, diagnostico):
        self.id_doctor = id_doctor
        self.id_paciente = id_paciente
        self.diagnostico = diagnostico

    def save(self):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO historial_citas (id_doctor, id_paciente, diagnostico)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    self.id_paciente,
                    self.id_paciente,
                    self.diagnostico,
                ),
            )
            conn.commit()

    @staticmethod
    def list_by_patient(patient_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 
                    historial_citas.id, 
                    doctores.nombre AS doctor_nombre, 
                    patients.name AS paciente_nombre, 
                    historial_citas.diagnostico
                FROM historial_citas
                JOIN doctores ON historial_citas.id_doctor = doctores.id
                JOIN patients ON historial_citas.id_paciente = patients.id
                WHERE historial_citas.id_paciente = ?
                """,
                (patient_id,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "doctor_nombre": row[1],
                    "paciente_nombre": row[2],
                    "diagnostico": row[3],
                }
                for row in rows
            ]
