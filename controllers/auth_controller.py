from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash

from models.usuario_model import obtener_usuario_por_correo, existe_correo, crear_usuario
from utils.validaciones import validar_correo, validar_password



auth_bp = Blueprint("auth", __name__)

def ruta_inicio(rol):
    if rol == "Administrador":
        return url_for("admin.usuarios_lista")
    return url_for("core.dashboard")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "usuario_id" in session:
        return redirect(ruta_inicio(session["rol"]))
    
    if request.method == "GET":
        return render_template("auth/login.html",correo="", error=None)
    
    correo, _ = validar_correo(request.form.get("correo")) 
    password = request.form.get("password","")
    usuario = obtener_usuario_por_correo(correo) if correo else None
    
    if not usuario or not check_password_hash(usuario["password_hash"],password):
        return render_template(
            "auth/login.html", correo=correo, error="Correo o contraseña incorrectos."
        ), 401
    
    session.clear()
    session["usuario_id"] = usuario["usuario_id"]
    session["nombre"] = usuario["nombre_usuario"]
    session["rol"] = usuario["rol"]
    return redirect(ruta_inicio(usuario["rol"]))

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("auth.login"))

@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if "usuario_id" in session:
        return redirect(ruta_inicio(session["rol"]))
    
    if request.method == "GET":
        return render_template("auth/registro.html", datos={}, errores=[])
    
    nombre = request.form.get("nombre", "").strip()
    apellido = request.form.get("apellido", "").strip()
    password = request.form.get("password","")
    confirmar = request.form.get("confirmar_password","")
    
    # Mismas validaciones de back-end que en el admin
    correo, errores = validar_correo(request.form.get("correo"))
    errores += validar_password(password)
    
    if password != confirmar:
        errores.append("Las contraseñas no coinciden.")
    
    if not nombre:
        errores.append("El nombre es obligatorio.")
    
    if len(nombre) > 50:
        errores.append("El nombre no debe ser mayor a 50 caracteres.")
        
    if not apellido:
        errores.append("El apellido es obligatorio.")
        
    if len(apellido) > 50:
        errores.append("El apellido no debe ser mayor a 50 caracteres.")
        
    if not correo or existe_correo(correo):
        errores.append("El correo ya existe.")
        
    if errores:
        return render_template("auth/registro.html", datos=request.form, errores=errores), 400
    
    # El registro publico siempre crea estudaintes: el rol no se lee del formulario
    crear_usuario(nombre, apellido, correo, password, "Estudiante", None)
    flash("Cuenta creada correctamente. Ya puedes iniciar sesión", "success")
    return redirect(url_for("auth.login"))