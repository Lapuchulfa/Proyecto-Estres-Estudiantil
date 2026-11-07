from database import obtener_conexion

def listar_alertas():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        Select a.alerta_id, a.estado, a.fecha, a.mensaje, u.nombre_usuario, u.apellido_usuario, t.nombre_tecnica
        from alerta a
        Join usuario u On u.usuario_id = a.usuario_id
        Join tecnica_manejo_estres t On t.tecnicaManejoEstres_id = a.tecnicaManejoEstres_id
        Order by a.fecha Desc
        """
    )
    alertas = cursor.fetchall()
    cursor.close()
    conn.close()
    return alertas
    
def crear_alerta(mensaje, fecha, usuario_id, tecnica_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        Insert into alerta (mensaje, fecha, usuario_id, tecnicaManejoEstres_id)
        Values (%s, %s, %s, %s)
        """,
        (mensaje, fecha, usuario_id, tecnica_id)
    )
    conn.commit()
    cursor.close()
    conn.close()