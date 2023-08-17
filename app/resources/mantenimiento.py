from flask import render_template, session
from app.helpers.permission import is_active


def index():
    """
    Muestra la pagina de mantenimiento.
    Si hay un usuario logueado y está bloqueado, lo desconecta
    y le muestra una pantalla que informa acceso no autorizado.
    """
    if "user" in session:
        is_active(session["user"])
    return render_template("mantenimiento.html")
