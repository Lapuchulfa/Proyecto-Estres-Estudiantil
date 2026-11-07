from database import obtener_conexion

def listar_tecnica_por_arquetipo(arquetipo_id):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        Select tecnicaManejoEstres_id, nombre_tecnica
        from tecnica_manejo_estres
        where arquetipo_id = %s
        order by nombre_tecnica
        """,
        (arquetipo_id,)
    )
    tecnicas = cursor.fetchall()
    cursor.close()
    conn.close()
    return tecnicas

def tecnica_de_arquetipo(tecnica_id, arquetipo_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        Select 1 from tecnica_manejo_estres
        where tecnicaManejoEstres_id = %s and arquetipo_id = %s
        """,
        (tecnica_id, arquetipo_id)
    )
    existe = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return existe