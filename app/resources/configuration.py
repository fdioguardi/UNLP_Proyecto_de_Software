from flask import redirect, render_template, request, url_for, abort, session
from app.services.validations.config_form import ConfigForm
from app.models.configuration import Configuration
from app.helpers.auth import authenticated
from app.helpers.permission import check as check_permission


# Protected resourse
def index():
    """
    Se encarga de mostrar informacion de configuracion de la página.
    - Aborta si no hay usuario autenticado.
    - Aborta si no tiene el permiso para acceder a configuration_index.
    - Si esta autenticado y tiene permiso rellena los datos del form con
    los datos de la configuracion pasada.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "configuration_index"):
        abort(401)
    form = ConfigForm()
    form.completarDatos(Configuration.getConfig())
    return render_template("configuration/index.html", form=form)


def update():
    """
    Se encarga de modificar datos de la configuracion de la pagina.
    - Aborta si no hay usuario autenticado.
    - Aborta si no tiene el permiso para acceder a configuration_update
    - Si el usuario esta autenticado y tiene permiso valida los datos
    del form:
    Si pasa la validacion lo modifica en la base de datos.
    Si no pasa la valdiacion recarga con los datos anteriores e
    informa los errores.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "configuration_update"):
        abort(401)
    form = ConfigForm(request.form)
    if form.validate():
        Configuration.modificar(
            form.titulo.data,
            form.descripcion.data,
            form.email.data,
            form.cantElement.data,
            form.habilitado.data,
        )
        return redirect(url_for("home"))
    return render_template("configuration/index.html", form=form)
