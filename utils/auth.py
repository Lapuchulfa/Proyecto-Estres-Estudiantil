from flask import session, redirect, url_for, flash


def exigir_rol(rol):
    if session.get("rol") != rol:
        flash("Debes iniciar sesión con una cuenta autorizada.", "mistake")
        return redirect(url_for("auth.login"))
    return None