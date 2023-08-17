from flask import redirect, render_template, request, url_for, session, abort
from app.models.role import Role
from app.helpers.auth import authenticated
from app.models.user import User
from app.services.validations.role_assign_form import RoleAssignForm
from app.services.validations.csrf_base_form import CsrfBaseForm
from app.helpers.permission import check as check_permission


def show():
    """
    Se encarga de mostrar los roles que determinado usuario
    tiene asignados.
    - Aborta si no hay usuario autenticado, si no hay id en argumentos,
    si el usuario de la sesion no tiene permisos para asignar roles y
    si no existe usuario con la id pasada.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "role_show"):
        abort(401)
    id = request.args.get("id")
    if not id:
        abort(404)
    user = User.find_by_id(id)
    if not user:
        abort(404)
    has_all = User.has_all_roles(user)
    return render_template(
        "role/show.html",
        user_roles=user.roles,
        username=user.username,
        has_all=has_all,
    )


def select():
    """
    Genera el formulario para la asignacion de rol
    a un usuario.
    - Aborta si no hay usuario autenticado, si no hay id en argumentos,
    si el usuario de la sesion no tiene permisos para asignar roles y
    si no existe usuario con la id pasada.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)

    if not check_permission(user_email, "role_select"):
        abort(401)

    id = request.args.get("id")
    if not id:
        abort(404)
    user = User.find_by_id(id)
    if not user:
        abort(404)

    roles_to_pick = Role.roles_missing_for(user)
    role_list = []
    for role in roles_to_pick:
        role_list.append((role.id, role.name))
    form = RoleAssignForm()
    form.role_choices(role_list)
    return render_template("role/assign.html", form=form)


def assign():
    """
    Se encarga de la validacion del formulario de asignacion de roles.
    - Aborta si no hay usuario autenticado, si no hay id en argumentos,
    si el usuario de la sesion no tiene permisos para asignar roles y
    si no existe usuario con la id pasada.
    Si valida: asigna el rol seleccionado al usuario y carga la relación
    a la base de datos, redireccionando al listado de roles del usuario.
    Si no valida: recarga el formulario con los datos anteriores
    e informa errores.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)

    if not check_permission(user_email, "role_assign"):
        abort(401)

    id = request.args.get("id")
    if not id:
        abort(404)
    user = User.find_by_id(id)
    if not user:
        abort(404)
    form = RoleAssignForm(request.form)
    roles_to_pick = Role.roles_missing_for(user)
    role_list = []
    for role in roles_to_pick:
        role_list.append((role.id, role.name))
    form.role_choices(role_list)
    if form.validate():
        User.assign_role_to(request.args.get("id"), int(form.role.data))
        return redirect(url_for("role_show", id=request.args.get("id")))

    return render_template("role/assign.html", form=form)


def delete():
    """
    Se encarga de quitarle un rol a un usuario.
    - Aborta si no hay usuario autenticado, si no hay id en argumentos,
    si se esta tratando de borrar el rol administrado de un usuario,
    si el usuario de la sesion no tiene permisos para borrar roles y
    si no existe usuario con la id pasada.
    - En GET carga un mensaje para confirmar la accion de borrar la
    relacion entre el usuario y el rol seleccionado
    - En POST elimina la relacion y retorna al listado de roles del
    usuario.
    Si no valida: recarga el formulario con los datos anteriores e
    informa errores.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)

    if request.args.get("role") == "Admin":
        abort(401)

    if not check_permission(user_email, "role_delete"):
        abort(401)

    user_id = request.args.get("id")
    if not user_id:
        abort(404)
    user = User.find_by_id(user_id)
    if not user:
        abort(404)

    if request.method == "GET":
        form = CsrfBaseForm()
        return render_template(
            "role/delete.html",
            user_name=request.args.get("user_name"),
            form=form,
        )

    if request.method == "POST":
        form = CsrfBaseForm(request.form)
        if form.validate():
            role = Role.find_by_name(request.args.get("role"))
            user.remove_role(role)
            return redirect(url_for("role_show", id=user_id))
        return render_template("role/show.html", id=user_id, form=form)
