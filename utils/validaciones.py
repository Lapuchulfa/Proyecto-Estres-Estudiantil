import re # esto es para poder usar expresiones regulares
from datetime import date, datetime

PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$") # expresion regular para validar correos    
ROLES_PERMITIDOS = ("Administrador","Estudiante")

# Rango de peso permitido para los distintos eventos que tenga el alumno en la semana
TIPOS_EVENTOS = {
    "Clase": (0.5, 1),
    "Quiz": (1,2),
    "Deber": (2,4),
    "Proyecto": (2,4), 
    "Examen": (3,5),
}

ESTADOS_EVENTO = ("Pendiente", "En progreso", "Completado")
DIAS_MAXIMOS = 180

NIVEL_ESTRES_MIN = 1
NIVEL_ESTRES_MAX = 10

def validar_correo(correo):
    errores = []
    correo = (correo or "").strip().lower()
    
    if not correo:
        errores.append("El correo no puede estar vacío.")
    elif len(correo) > 100:
        errores.append("El correo no puede tener más de 100 caracteres.")
    elif not PATRON_CORREO.match(correo):
        errores.append("El correo no tiene un formato válido.")
    return correo, errores

def validar_password(password):
    errores = []
    password = password or ""
    
    if len(password) < 8:
        errores.append("La contraseña debe tener al menos 8 caracteres.")
    if not re.search(r"[A-Z]", password): # re.search busca un patrón en la cadena, en este caso busca una letra mayúscula
        errores.append("La contraseña debe contener al menos una letra mayúscula.")
    if not re.search(r"[a-z]", password):
        errores.append("La contraseña debe contener al menos una letra minúscula.")
    if not re.search(r"\d", password):
        errores.append("La contraseña debe contener al menos un número.")
    return errores

def validar_rol(rol):
    if rol not in ROLES_PERMITIDOS:
        return ["El rol seleccionado no es válido."]
    return []

def validar_evento(materia, tipo, peso, fecha, estado):
    errores = []
    
    materia = (materia or "").strip()
    
    if not materia or len(materia) > 20:
        errores.append("La materia es obligatoria y no puede superar los 20 caracteres.")
        
    if tipo not in TIPOS_EVENTOS:
        errores.append("El tipo de evento no es válido.")
        
    try:
        peso = float(peso)
    except (TypeError, ValueError):
        errores.append("El peso debe ser un número válido.")
        peso = None  # aqui se asigna None para evitar errores posteriores si el peso no es un número
        
    if peso is not None and tipo in TIPOS_EVENTOS:
        minimo, maximo = TIPOS_EVENTOS[tipo]
        
        if not minimo <= peso <= maximo:
            errores.append(f"El peso de un evento de tipo '{tipo}' debe estar entre {minimo} y {maximo}.")
            
    try:
        fecha = datetime.strptime(fecha or "", "%Y-%m-%d").date()
    except ValueError:
        errores.append("La fecha no tiene un formato válido (YYYY-MM-DD).")
        fecha = None  # aqui se asigna None para evitar errores posteriores si la fecha no es válida
        
    if fecha and abs((fecha - date.today()).days) > DIAS_MAXIMOS: # aqui se valida que la fecha del evento no esté a más de 6 meses (180 días) de la fecha actual
        errores.append("La fecha del evento debe estar dentro de los 6 meses anteriores o posteriores a la fecha actual.")
        
    if estado not in ESTADOS_EVENTO:
        errores.append("El estado del evento no es válido.")
        
    evento = {
        "materia": materia,
        "tipo": tipo,
        "peso": peso,
        "fecha": fecha,
        "estado": estado
    }
    return evento, errores
    
def validar_nivel_estres(nivel):
    try:
        nivel = int(nivel)
    except (TypeError, ValueError):
        return None, ["El nivel de estrés debe ser un número entero."]
    if not NIVEL_ESTRES_MIN <= nivel <= NIVEL_ESTRES_MAX:
        return nivel, [f"El nivel de estrés debe estar entre {NIVEL_ESTRES_MIN} y {NIVEL_ESTRES_MAX}."]
    
    return nivel, []

