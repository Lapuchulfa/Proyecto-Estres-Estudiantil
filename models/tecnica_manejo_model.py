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

def listar_tecnicas():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT t.tecnicaManejoEstres_id, t.nombre_tecnica, t.descripcion, t.es_predeterminada, a.nombre_arquetipo
        FROM tecnica_manejo_estres t
        JOIN arquetipo a ON a.arquetipo_id = t.arquetipo_id
        ORDER BY a.nombre_arquetipo, t.nombre_tecnica
        """
    )
    tecnicas = cursor.fetchall()
    cursor.close()
    conn.close()
    return tecnicas


def existe_tecnica_en_arquetipo(nombre, arquetipo_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 1 FROM tecnica_manejo_estres
        WHERE LOWER(nombre_tecnica) = LOWER(%s) AND arquetipo_id = %s 
        """,
        (nombre, arquetipo_id) 
    )
    existe = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return existe


def crear_tecnica(nombre, descripcion, arquetipo_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO tecnica_manejo_estres (nombre_tecnica, descripcion, arquetipo_id)
        VALUES (%s, %s, %s)
        """,
        (nombre, descripcion, arquetipo_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
def obtener_tecnica(tecnica_id):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT tecnicaManejoEstres_id, es_predeterminada
        FROM tecnica_manejo_estres
        WHERE tecnicaManejoEstres_id = %s
        """,
        (tecnica_id,)
    )
    tecnica = cursor.fetchone()
    cursor.close()
    conn.close()
    return tecnica


def tecnica_en_uso(tecnica_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM alerta WHERE tecnicaManejoEstres_id = %s LIMIT 1",
        (tecnica_id,)
    )
    en_uso = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return en_uso


def eliminar_tecnica(tecnica_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM tecnica_manejo_estres
        WHERE tecnicaManejoEstres_id = %s AND es_predeterminada = FALSE
        """,
        (tecnica_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()

