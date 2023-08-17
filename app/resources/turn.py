from flask import redirect, render_template, request, url_for, session, abort
from app.helpers.auth import authenticated
from app.helpers.permission import check as check_permission
from app.models.center import Center
from app.services.validations.turn_delete_form import TurnDeleteForm
from app.services.validations.turn_search_form import TurnSearchForm
from app.models.turn import Turn
from app.models.configuration import Configuration
from datetime import date


def index():
    """
    Se encarga de mostrar el listado de turnos para un centro.
    - Aborta si no hay usuario autenticado y si el usuario
    de la sesion no tiene permisos para ver los turnos.
    - Aborta si no pasaste id de centro.
    - Aborta si no existe un centro con la id pasada.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "turn_index"):
        abort(401)
    center_id = request.args.get("id")
    if not center_id:
        abort(404)
    center = Center.find_by_id(center_id)
    if not center:
        abort(404)
    page = request.args.get("page", default=1, type=int)
    turns = Turn.paginated_turns_from(
        center_id, Configuration.items_per_page(), page
    )
    del_form = TurnDeleteForm()
    return render_template(
        "turn/index.html",
        turns=turns,
        center_name=center.name,
        delete_form=del_form,
    )


def new():
    """
    Genera el formulario para creacion de turnos.
    - Aborta si no hay usuario autenticado y si el usuario de la sesion
    no tiene permisos para crear usuarios.
    - Aborta si no pasaste id de centro.
    - Aborta si no existe un centro con la id pasada.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "turn_create"):
        abort(401)
    center_id = request.args.get("id")
    if not center_id:
        abort(404)
    center = Center.find_by_id(center_id)
    if not center:
        abort(404)
    return render_template(
        "turn/new.html", id=center_id, name=center.name, hoy=date.today()
    )


def delete():
    """
    Se encarga borrar turnos del sistema.
    - Aborta si no hay usuario autenticado y si el usuario de la sesion
    no tiene permisos para crear usuarios.
    - Aborta si no pasaste id de turno.
    - Aborta si no existe un turno con la id pasada.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "turn_delete"):
        abort(401)

    form = TurnDeleteForm(request.form)

    turn_id = int(form.turn_id.data)

    if not turn_id:
        abort(404)

    turn = Turn.find_by_id(turn_id)

    center_id = turn.center_id

    if not turn:
        abort(404)

    if form.validate():
        Turn.delete(turn)

    comes_from_index = request.args.get("index")

    if comes_from_index:
        return redirect(url_for("turn_index", id=center_id))
    return redirect(
        url_for(
            "turn_search",
            search=request.args.get("search", default="", type=str),
            select=request.args.get("select", default="", type=str),
        )
    )


def search():
    """
    Se encarga de mostrar un listado de turnos aplicando
    filtros de nombre de centro y el email de la persona
    que pidio el turno.
    Aborta si no hay usuario autenticado y si el usuario de la sesion
    no tiene permisos para crear usuarios.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "turn_search"):
        abort(401)

    page = request.args.get("page", default=1, type=int)
    form = TurnSearchForm()
    substring = request.args.get("search")
    select_center = request.args.get("select")
    centers = Center.get_all()
    if substring or select_center:
        form.add_data(substring, select_center)
        if substring and select_center:
            turns = Turn.search_by_email_and_center(
                page,
                Configuration.items_per_page(),
                email=substring,
                c_name=select_center,
            )
        elif substring:
            turns = Turn.search_by_email(
                page, Configuration.items_per_page(), email=substring
            )
        elif select_center:
            turns = Turn.search_by_center(
                page, Configuration.items_per_page(), c_name=select_center
            )
    else:
        turns = Turn.paginated_turns(page, Configuration.items_per_page())

    return render_template(
        "turn/search.html",
        turns=turns,
        search_form=form,
        delete_form=TurnDeleteForm(),
        centers=centers,
    )
