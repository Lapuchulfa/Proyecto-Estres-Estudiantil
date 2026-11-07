from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.arquetipo_model import listar_arquetipos, existe_arquetipo
from models.evento_academico_model import crear_evento, listar_eventos
from models.usuario_model import listar_usuarios, crear_usuario, existe_correo, listar_estudiantes, es_estudiante
from utils.validaciones import (
    validar_correo, validar_password, validar_rol, ROLES_PERMITIDOS,
    validar_evento, TIPOS_EVENTOS, ESTADOS_EVENTO,
)
from utils.auth import exigir_rol

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


#Eventos Académicos

def mostrar_formulario_evento(datos, errores, status=200):
    return render_template(
        "admin/evento_form.html",
        estudiantes = listar_estudiantes(),
        tipos = TIPOS_EVENTOS,
        estados = ESTADOS_EVENTO,
        datos=datos,
        errores=errores,
    ), status
    
@admin_bp.route("/eventos")
def eventos_lista():
    return render_template("admin/eventos_lista.html", eventos=listar_eventos())


@admin_bp.route("/eventos/nuevo", methods=["GET", "POST"])
def evento_nuevo():
    if request.method == "GET":
        return mostrar_formulario_evento({}, [])

    # Validación en back-end del dato sensible del core: el peso del evento
    evento, errores = validar_evento(
        request.form.get("materia"),
        request.form.get("tipo"),
        request.form.get("peso"),
        request.form.get("fecha"),
        request.form.get("estado"),
    )

    usuario_id = request.form.get("usuario_id")
    if not usuario_id or not es_estudiante(usuario_id):
        errores.append("Debe seleccionar un estudiante válido.")

    if errores:
        return mostrar_formulario_evento(request.form, errores, 400)

    crear_evento(evento["materia"], evento["tipo"], evento["fecha"],
                 evento["peso"], evento["estado"], usuario_id)
    flash("Evento académico creado correctamente.", "success")
    return redirect(url_for("admin.eventos_lista"))