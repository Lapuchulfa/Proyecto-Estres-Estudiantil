from database import obtener_conexion

def listar_eventos():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        Select e.eventoAcademico_id, e.materia, e.tipo, e.fecha, e.peso, e.estado, u.nombre_usuario, u.apellido_usuario
        from evento_academico e
        join usuario u On u.usuario_id = e.usuario_id
        Order by e.fecha
        """
    )
    eventos = cursor.fetchall() # fetchall() devuelve una lista de diccionarios, donde cada diccionario representa una fila de la tabla evento_academico
    cursor.close()
    conn.close()
    return eventos

def crear_evento(materia, tipo, fecha, peso, estado, usuario_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        Insert into evento_academico (materia, tipo, fecha, peso, estado, usuario_id)
        Values (%s, %s, %s, %s, %s, %s)
        """,
        (materia, tipo, fecha, peso, estado, usuario_id)
    )
    conn.commit()
    cursor.close()
    conn.close()