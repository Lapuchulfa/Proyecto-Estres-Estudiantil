from flask import Blueprint, render_template, session
from utils.auth import exigir_rol
from models.alerta_model import listar_alertas_de_usuario

core_bp = Blueprint("core", __name__, url_prefix="/core")

@core_bp.before_request
def proteger_core():
    return exigir_rol("Estudiante")

@core_bp.route("/dashboard")
def dashboard():
    return render_template(
        "core/dashboard.html",
        nombre=session["nombre"],
        alertas=listar_alertas_de_usuario(session["usuario_id"]),
    )