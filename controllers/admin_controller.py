from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.arquetipo_model import listar_arquetipos, existe_arquetipo
from models.evento_academico_model import listar_eventos
from models.usuario_model import listar_usuarios, crear_usuario, existe_correo, listar_estudiantes_por_arquetipo, estudiante_de_arquetipo
from utils.validaciones import (
    validar_correo, validar_password, validar_rol, ROLES_PERMITIDOS
)
from utils.auth import exigir_rol
from datetime import date
from models.tecnica_manejo_model import listar_tecnica_por_arquetipo, tecnica_de_arquetipo
from models.alerta_model import listar_alertas, crear_alerta


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

#
@admin_bp.before_request
def proteger_admin():
    return exigir_rol("Administrador")

# Usuarios

def mostrar_formulario_usuario(datos, errores, status=200):
    return render_template(
        "admin/usuario_form.html",
        arquetipos=listar_arquetipos(),
        roles=ROLES_PERMITIDOS,
        datos=datos,
        errores=errores,
    ), status
    
@admin_bp.route('/usuarios')
def usuarios_lista():
    return render_template("admin/usuarios_lista.html", usuarios=listar_usuarios())


@admin_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
def usuarios_nuevo():
    if request.method == 'GET':
        return mostrar_formulario_usuario({}, [])
    
    nombre = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    password = request.form.get('password', '')
    rol = request.form.get('rol', '').strip()
    arquetipo_id = request.form.get('arquetipo_id') or None
    
    #Validacion de back.end del dato sensible correo y password
    correo, errores = validar_correo(request.form.get("correo"))
    errores += validar_password(password)
    errores += validar_rol(rol)
    
    if rol == "Administrador":
        arquetipo_id = None

    if not nombre or len(nombre) > 50:
        errores.append("El nombre es obligatorio y no puede superar los 50 caracteres.")
    
    if not apellido or len(apellido) > 50:
        errores.append("El apellido es obligatorio y no puede superar los 50 caracteres.")
        
    if arquetipo_id and not existe_arquetipo(arquetipo_id):
        errores.append("El arquetipo seleccionado no existe.")
    
    if not errores and existe_correo(correo):
        errores.append("El correo electrónico ya está registrado.")
    
    if errores:
        return mostrar_formulario_usuario(request.form, errores, status=400)
    
    crear_usuario(nombre, apellido, correo, password, rol, arquetipo_id)
    flash("Usuario creado exitosamente.", "success")
    return redirect(url_for('admin.usuarios_lista'))
    
@admin_bp.route("/eventos")
def eventos_lista():
    return render_template("admin/eventos_lista.html", eventos=listar_eventos())

#Alertas

def mostrar_formulario_alerta(datos, errores, status=200):
    arquetipo_id = datos.get("arquetipo_id")
    return render_template(
        "admin/alerta_form.html",
        arquetipos = listar_arquetipos(),
        estudiantes = listar_estudiantes_por_arquetipo(arquetipo_id) if arquetipo_id else [],
        tecnicas = listar_tecnica_por_arquetipo(arquetipo_id) if arquetipo_id else [],
        datos = datos,
        errores = errores,
    ), status
    
@admin_bp.route("/alertas")
def alertas_lista():
    return render_template("admin/alertas_lista.html", alertas=listar_alertas())

@admin_bp.route("/alertas/nueva", methods=["GET", "POST"])
def alerta_nueva():
    # # GET: si viene ?arquetipo_id=X en la URL, se cargan sus estudiantes y técnicas
    if request.method == "GET":
        return mostrar_formulario_alerta(request.args, [])
    
    arquetipo_id = request.form.get("arquetipo_id")
    usuario_id = request.form.get("usuario_id")
    tecnicaa_id = request.form.get("tecnica_id")
    mensaje = request.form.get("mensaje", "").strip()
    errores = []
    
    #Validacion back-end estudiante y tecnicas deben pertenecer al mismo arquetipo
    if not arquetipo_id or not existe_arquetipo(arquetipo_id):
        errores.append("Debe seleccionar un arquetipo valido.")
    else:
        if not usuario_id or not estudiante_de_arquetipo(usuario_id, arquetipo_id):
            errores.append("El estudiante no pertenece al arquetipo seleccionado.")
        if not tecnicaa_id or not tecnica_de_arquetipo(tecnicaa_id, arquetipo_id):
            errores.append("La técnica no corresponde al arquetipo seleccionado.")

    if not mensaje or len(mensaje) > 100:
        errores.append("El mensaje debe ser obligatorio y no puede superar los 100 caracteres.")
        
    if errores:
        return mostrar_formulario_alerta(request.form, errores, 400)
    
    crear_alerta(mensaje, date.today(), usuario_id, tecnicaa_id)
    flash("Alerta de seguimiento creada correctamente.", "success")
    return redirect(url_for("admin.alertas_lista"))
    