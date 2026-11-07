from database import obtener_conexion

def listar_arquetipos():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary = True)
    cursor.execute(
        """Select arquetipo_id, nombre_arquetipo 
        from arquetipo 
        Order by nombre_arquetipo """
    )
    arquetipos = cursor.fetchall() # fetchall() devuelve una lista de diccionarios, donde cada diccionario representa una fila de la tabla arquetipo
    cursor.close()
    conn.close()
    return arquetipos

def existe_arquetipo(arquetipo_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        Select 1 
        from arquetipo 
        where arquetipo_id = %s
        """,
        (arquetipo_id,)
    )
    existe = cursor.fetchone() is not None # fetchone() devuelve None si no hay resultados, por lo que si devuelve algo, significa que el arquetipo existe
    cursor.close()
    conn.close()
    return existe
    