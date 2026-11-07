from werkzeug.security import generate_password_hash
from database import obtener_conexion

def listar_usuarios():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        Select u.usuario_id, u.nombre_usuario, u.apellido_usuario, u.correo_usuario, u.rol, a.nombre_arquetipo
        from usuario u
        left join arquetipo a On a.arquetipo_id = u.arquetipo_id
        Order by u.apellido_usuario, u.nombre_usuario
        """  
    )
    usuarios = cursor.fetchall() # fetchall() devuelve una lista de diccionarios, donde cada diccionario representa una fila de la tabla usuario
    cursor.close()
    conn.close()
    return usuarios

def existe_correo(correo):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        Select 1
        from usuario
        where correo_usuario = %s
        """,
        (correo,) # Se pasa el correo como una tupla para evitar inyecciones SQL
    )
    existe = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return existe

def crear_usuario(nombre, apellido, correo, password, rol, arquetipo_id):
    password_hash = generate_password_hash(password) # Se genera el hash de la contraseña
    
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        Insert into usuario (nombre_usuario, apellido_usuario, correo_usuario, password_hash, rol, arquetipo_id)
        Values (%s, %s, %s, %s, %s, %s)
        """,
        (nombre, apellido, correo, password_hash, rol, arquetipo_id), # Se pasa el hash de la contraseña en lugar de la contraseña en texto plano
    )
    conn.commit()
    cursor.close()
    conn.close()
    
def listar_estudiantes():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        Select usuario_id, nombre_usuario, apellido_usuario, correo_usuario
        from usuario
        where rol = 'Estudiante'
        Order by apellido_usuario, nombre_usuario
        """
    )
    estudiantes = cursor.fetchall()
    cursor.close()
    conn.close()
    return estudiantes

def es_estudiante(usuario_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        Select 1
        from usuario
        where usuario_id = %s and rol = 'Estudiante'
        """,
        (usuario_id,)
    )
    existe = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return existe

def obtener_usuario_por_correo(correo):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        Select usuario_id, nombre_usuario, password_hash, rol
        from usuario
        where correo_usuario = %s
        """,
        (correo,)
    )
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario