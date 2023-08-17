from flask import redirect, render_template, request, url_for, session, abort
from app.models.user import User
from app.helpers.auth import authenticated
from app.services.validations.user_search_form import UserSearchForm
from app.services.validations.user_creation_form import UserCreationForm
from app.services.validations.user_edit_form import UserEditForm
from app.services.validations.user_state_form import UserStateForm
from app.services.validations.user_delete_form import UserDeleteForm
from app.helpers.permission import check as check_permission
from app.models.configuration import Configuration


def index():
    """
    Se encarga de mostrar el listado de usuarios.
    - Aborta si no hay usuario autenticado y si el usuario
    de la sesion no tiene permisos para ver los usuarios.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "user_index"):
        abort(401)

    page = request.args.get("page", default=1, type=int)
    form = UserSearchForm()
    substring = request.args.get("search")
    select_state = request.args.get("select")

    if substring or select_state:

        form.add_data(substring, select_state)

        if select_state == "Activo":
            users = User.search_by_username_and_state(
                page,
                Configuration.items_per_page(),
                username=substring,
                active=True,
            )

        elif select_state == "Bloqueado":
            users = User.search_by_username_and_state(
                page,
                Configuration.items_per_page(),
                username=substring,
                active=False,
            )
        else:
            users = User.search_by_username(
                page, Configuration.items_per_page(), substring
            )

    else:
        users = User.paginate(page, Configuration.items_per_page())

    return render_template(
        "user/index.html",
        users=users,
        search_form=form,
        state_form=UserStateForm(),
        delete_form=UserDeleteForm(),
    )


def new():
    """
    Genera el formulario para creacion de usuarios.
    - Aborta si no hay usuario autenticado y si el usuario de la sesion
    no tiene permisos para crear usuarios.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "user_new"):
        abort(401)
    form = UserCreationForm()
    return render_template("user/new.html", form=form)


# POST
def create():
    """
    Se encarga de la validacion del formulario de creacion de usuarios.
    - Aborta si no hay usuario autenticado y si el usuario de la sesion
    no tiene permisos para crear usuarios
    Si valida: crea el usuario y lo carga en la base de datos.
    Si no valida: recarga el formulario con los datos anteriores
    e informa errores
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "user_create"):
        abort(401)
    form = UserCreationForm(request.form)
    if form.validate():
        User.create(
            User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data,
                username=form.username.data,
                active=form.active.data,
            )
        )
        return redirect(url_for("user_index"))
    return render_template("user/new.html", form=form)


def edit():
    """
    Se encarga de la edicion de usuarios.
    - Aborta si no hay usuario autenticado, si no hay id en argumentos,
    si no existe usuario con la id pasada y si el usuario de la
    sesión no tiene permisos para editar usuarios.
    - En GET rellena los datos del form con los datos del usuario
    pasado.
    - En POST valida los datos del form: si valida updatea el usuario
    en la bse de datos. En caso contrario recarga con los datos
    anteriores e informa errores.
    """

    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "user_edit"):
        abort(401)
    user_id = request.args.get("id")
    if not user_id:
        abort(404)
    user = User.find_by_id(user_id)
    if not user:
        abort(404)
    if request.method == "GET":
        form = UserEditForm()
        form.complete_data(user)
    if request.method == "POST":
        form = UserEditForm(request.form)
        if form.validate():
            if user == User.find_by_email(session["user"]):
                session["user"] = form.email.data
            user = User.update_user_by_id(
                user_id,
                form.email.data,
                form.password.data,
                form.first_name.data,
                form.last_name.data,
                form.username.data,
            )
            return redirect(url_for("user_index"))

    return render_template("user/edit.html", form=form)


def state():
    """
    Se encarga de bloquear y desbloquear al usuario enviado por
    parametro.
    - Aborta si no hay usuario autenticado, si no hay id en argumentos,
    si no existe usuario con la id pasada y si el usuario de la sesion
    no tiene permisos para bloquear/desbloquear usuarios.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "user_state"):
        abort(401)

    form = UserStateForm(request.form)
    user_id = int(form.user_id.data)

    if not user_id:
        abort(404)

    user = User.find_by_id(user_id)

    if not user:
        abort(404)

    if user.user_has_role("Admin"):
        abort(401)

    if form.validate():
        user.change_state()

    return redirect(url_for("user_index"))


def delete():
    """
    Se encarga borrar usuarios del sistema.
    - Aborta si no hay usuario autenticado, si no hay id en argumentos,
    si no existe usuario con la id pasada y si el usuario de la sesion
    no tiene permisos para bloquear/desbloquear usuarios.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "user_delete"):
        abort(401)

    form = UserDeleteForm(request.form)

    user_id = int(form.user_id.data)

    if not user_id:
        abort(404)

    user = User.find_by_id(user_id)

    if not user:
        abort(404)

    if user.user_has_role("Admin"):
        abort(401)

    if form.validate():
        User.delete(user)

    return redirect(url_for("user_index"))
