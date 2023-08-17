from app.models.user import User
from flask import redirect, render_template, request, url_for, session, flash
from app.services.validations.user_login_form import UserLoginForm
from app.helpers.configuration import is_enabled
from app.helpers.permission import is_active

# GET
def login():
    """
    Se encarga de mostrar el formulario para iniciar sesión.
    """
    form = UserLoginForm()
    return render_template("auth/login.html", form=form)


# POST
def authenticate():
    """
    Se encarga de la autenticación del formulario para iniciar sesión.
    Si el formulario valida:
    - Si la página no está activa y el usuario no es 'Admin': no inicia
    sesión y muestra la página de mantenimiento.
    - Si la página está activa: inicia sesión y muestra la página home.
    - Si el usuario está bloqueado: lo desconecta y le muestra una
    pantalla que informa acceso no autorizado.
    """
    form = UserLoginForm(request.form)
    if form.validate():
        if (not is_enabled()) and (
            not User.has_role(form.email.data, "Admin")
        ):
            return redirect(url_for("mantenimiento"))
        session["user"] = form.email.data
        is_active(form.email.data)
        flash("La sesión se inició correctamente.")
        return redirect(url_for("home"))
    return render_template("auth/login.html", form=form)


def logout():
    """
    Se encarga de cerrar la sesión del usuario y redirigir a la
    página de inicio de sesión.
    """
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("home"))
