import sqlite3  # Para interactuar con la base de datos SQLite
from werkzeug.security import generate_password_hash


def initialize_database():
    """
    Inicializa la base de datos creando las tablas necesarias.
    """
    # Conectar a la base de datos (se crea automáticamente si no existe)
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Crear la tabla de usuarios (si no existe)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        id_doctor INTEGER,
        id_paciente INTEGER,
        role TEXT NOT NULL
    )
    """
    )

    # Crear la tabla de doctores (si no existe)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS doctores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        fecha_nacimiento TEXT NOT NULL,
        sexo TEXT NOT NULL,
        cedula TEXT UNIQUE NOT NULL,
        nro_carnet TEXT UNIQUE NOT NULL,
        clave TEXT NOT NULL,
        especialidad TEXT NOT NULL
    );
    """
    )

    # Crear la tabla de especialidades (si no existe)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS especialidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_especialidad TEXT UNIQUE NOT NULL
    );
    """
    )

    # Crear la tabla de relaciones doctor-especialidad (si no existe)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS doctor_especialidades (
        doctor_id INTEGER NOT NULL,
        especialidad_id INTEGER NOT NULL,
        PRIMARY KEY (doctor_id, especialidad_id),
        FOREIGN KEY (doctor_id) REFERENCES doctores(id),
        FOREIGN KEY (especialidad_id) REFERENCES especialidades(id)
    );
    """
    )

    # Crear la tabla de pacientes (si no existe)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        identificacion_tipo TEXT NOT NULL,
        identificacion_numero TEXT NOT NULL,
        telefono TEXT NOT NULL,
        direccion TEXT NOT NULL,
        descendencia TEXT NOT NULL,
        nombre_hijo TEXT,
        fecha_nacimiento_hijo TEXT,
        sexo_hijo TEXT,
        fecha_nacimiento TEXT NOT NULL,
        sexo TEXT NOT NULL,
        patologia TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """
    )

    # Crear la tabla de citas (si no existe)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS citas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER NOT NULL,
        patient_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        motivo TEXT NOT NULL,
        atendida INTEGER DEFAULT 0, -- Nuevo campo para indicar si la cita fue atendida
        FOREIGN KEY (doctor_id) REFERENCES doctores(id),
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    );
    """
    )

    # Insertar un usuario por defecto si no existe
    cursor.execute(
        """
    INSERT INTO users (username, password, role)
    SELECT 'admin', 'admin123', 'admin'
    WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'admin');
    """
    )

    # Insertar un doctor por defecto si no existe
    cursor.execute(
        """
    INSERT INTO doctores (nombre, fecha_nacimiento, sexo, cedula, nro_carnet, clave, especialidad)
    SELECT 'Doctor Default', '1980-01-01', 'masculino', '12345678', '000001', 'clave123', 'General'
    WHERE NOT EXISTS (SELECT 1 FROM doctores WHERE cedula = '12345678');
    """
    )

    # Insertar un paciente por defecto si no existe
    cursor.execute(
        """
    INSERT INTO patients (user_id, name, identificacion_tipo, identificacion_numero, telefono, direccion, descendencia, nombre_hijo, fecha_nacimiento_hijo, sexo_hijo, fecha_nacimiento, sexo, patologia)
    SELECT 1, 'Paciente Default', 'V', '87654321', '0987654321', 'Default Address', 'no', NULL, NULL, NULL, '1990-01-01', 'femenino', NULL
    WHERE NOT EXISTS (SELECT 1 FROM patients WHERE identificacion_numero = '87654321');
    """
    )
    # Crear la tabla de usuarios (si no existe)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """
    )
    # Crear la tabla de historial de citas (si no existe)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS historial_citas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cita INTEGER NOT NULL,
        id_paciente INTEGER NOT NULL,
        id_doctor INTEGER NOT NULL,
        diagnostico TEXT NOT NULL,
        FOREIGN KEY (id_cita) REFERENCES citas(id),
        FOREIGN KEY (id_paciente) REFERENCES patients(id),
        FOREIGN KEY (id_doctor) REFERENCES doctores(id)
    );
    """
    )
    # Insertar usuarios por defecto con contraseñas encriptadas si no existen
    default_users = [
        ("admin", "admin", "doctor", 1, 1),
        ("doctor", "doctor", "doctor", 0, 1),
        ("paciente", "paciente", "paciente", 1, 0),
    ]

    for username, plain_password, role, id_paciente, id_doctor in default_users:
        hashed_password = generate_password_hash(plain_password)
        cursor.execute(
            """
        INSERT INTO users (username, password, role, id_paciente, id_doctor)
        SELECT ?, ?, ?, ?, ?
        WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = ?);
        """,
            (username, hashed_password, role, id_paciente, id_doctor, username),
        )

        # Crear la tabla de horarios del doctor (si no existe)
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS horarios_doctor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER NOT NULL,
        dia TEXT NOT NULL,
        hora_inicio TEXT NOT NULL,
        hora_fin TEXT NOT NULL,
        FOREIGN KEY (doctor_id) REFERENCES doctores(id)
    );
    """
    )
    # Insertar un horario por defecto para el doctor por defecto si no existe
    default_schedule = [
        ("lunes", "08:00", "16:00"),
        ("martes", "08:00", "16:00"),
        ("miércoles", "08:00", "16:00"),
        ("jueves", "08:00", "16:00"),
        ("viernes", "08:00", "16:00"),
    ]

    for dia, hora_inicio, hora_fin in default_schedule:
        cursor.execute(
            """
        INSERT INTO horarios_doctor (doctor_id, dia, hora_inicio, hora_fin)
        SELECT 1, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM horarios_doctor
            WHERE doctor_id = 1 AND dia = ?
        );
        """,
            (dia, hora_inicio, hora_fin, dia),
        )

    # Insertar un paciente por defecto si no existe
    cursor.execute(
        """
    INSERT INTO patients (user_id, name, identificacion_tipo, identificacion_numero, telefono, direccion, descendencia, nombre_hijo, fecha_nacimiento_hijo, sexo_hijo, fecha_nacimiento, sexo, patologia)
    SELECT 1, 'Paciente Default', 'V', '87654321', '0987654321', 'Default Address', 'no', NULL, NULL, NULL, '1990-01-01', 'femenino', NULL
    WHERE NOT EXISTS (SELECT 1 FROM patients WHERE identificacion_numero = '87654321');
    """
    )
    # Insertar una cita por defecto para el paciente por defecto si no existe
    cursor.execute(
        """
    INSERT INTO citas (doctor_id, patient_id, fecha, motivo, atendida)
    SELECT 1, 1, '2025-03-26', 'Consulta inicial', 0
    WHERE NOT EXISTS (
        SELECT 1 FROM citas WHERE doctor_id = 1 AND patient_id = 1 AND fecha = '2025-03-26'
    );
    """
    )
    # Insertar un historial de citas por defecto para el paciente por defecto si no existe
    cursor.execute(
        """
    INSERT INTO historial_citas (id_cita, id_paciente, id_doctor, diagnostico)
    SELECT 1, 1, 1, 'Diagnóstico inicial'
    WHERE NOT EXISTS (SELECT 1 FROM historial_citas WHERE id_cita = 1 AND id_paciente = 1 AND id_doctor = 1);
    """
    )
    # Guardar los cambios en la base de datos
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()
