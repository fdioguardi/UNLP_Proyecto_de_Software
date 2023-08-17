from flask import redirect, render_template, url_for, session, abort
from app.models.center import Center
from app.models.center_state import CenterState
from app.models.center_type import CenterType
from app.helpers.auth import authenticated
from app.helpers.permission import check as check_permission
from app.models.configuration import Configuration
from app.services.validations.center_form import CenterForm
from app.services.validations.center_search_form import CenterSearchForm
from app.services.validations.center_delete_form import CenterDeleteForm
from app.services.validations.center_certify_form import CenterCertifyForm
from flask import request, current_app
import os, app, uuid, datetime
from werkzeug.utils import secure_filename
from app.helpers.turn_deleter import delete_turns


def index():
    """
    Se encarga de mostrar los centros.
    - Aborta si el usuario no está autenticado.
    - Aborta si el usuario no tiene permiso.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "center_index"):
        abort(401)

    aux_center_types = CenterType.get_all()
    center_types = {}
    for center_type in aux_center_types:
        center_types[center_type.id] = center_type.name

    page = request.args.get("page", default=1, type=int)
    form = CenterSearchForm()
    substring = request.args.get("search")
    select_state = request.args.get("select")

    if substring or select_state:
        form.add_data(substring, select_state)
        if select_state == "Aprobado":
            centers = Center.search_by_name_and_state(
                state=CenterState.find_by_name("Aprobado").id,
                page=page,
                limit=Configuration.items_per_page(),
                name=substring,
            )

        elif select_state == "Rechazado":
            centers = Center.search_by_name_and_state(
                state=CenterState.find_by_name("Rechazado").id,
                page=page,
                limit=Configuration.items_per_page(),
                name=substring,
            )

        elif select_state == "Pendiente":
            centers = Center.search_by_name_and_state(
                state=CenterState.find_by_name("Pendiente").id,
                page=page,
                limit=Configuration.items_per_page(),
                name=substring,
            )
        else:
            centers = Center.search_by_name_and_state(
                state="",
                page=page,
                limit=Configuration.items_per_page(),
                name=substring,
            )
    else:
        centers = Center.paginate(page, Configuration.items_per_page())

    return render_template(
        "center/index.html",
        centers=centers,
        tiposDeCentro=center_types,
        search_form=form,
        delete_form=CenterDeleteForm(),
        reject_form=CenterCertifyForm(),
        accept_form=CenterCertifyForm(),
    )


def create():
    """
    Se encarga de la validacion del formulario de creacion de centros.
    - Aborta si no hay usuario autenticado y si el usuario de la sesion
    no tiene permisos para crear centros
    Si valida: crea el centros y lo carga en la base de datos.
    Si no valida: recarga el formulario con los datos anteriores
    e informa errores
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "center_create"):
        abort(401)
    form_validate = CenterForm()
    filename = file = request.files["archivo"].filename
    form_validate.llenarDatos(request.form, filename)

    form = request.form

    all_center_types = CenterType.get_all()
    aux_center_types = []
    for center_type in all_center_types:
        aux_center_types.append(center_type.name)

    if not (form_validate.validate()):
        form = __crearFormulario(
            form["name"],
            form["address"],
            form["phone"],
            form["opens"],
            form["closes"],
            form["town_id"],
            form["web"],
            form["email"],
            "",
            form["lng"],
            form["lat"],
            form["center_type"],
            aux_center_types,
        )
        return render_template(
            "center/new.html", form_validate=form_validate, form=form
        )
    else:
        name = ""
        try:
            file = request.files["archivo"]
            name_file_new = ""
            if file.filename != "":
                filename = secure_filename(file.filename)
                images_dir = current_app.config["UPLOAD_PROTOCOL_DEST"]
                os.makedirs(images_dir, exist_ok=True)
                file_path = os.path.join(images_dir, filename)
                file.save(file_path)
                name = str(uuid.uuid4()) + ".pdf"
                while os.path.exists(name):
                    name = str(uuid.uuid4()) + ".pdf"
                name_file_new = os.path.join(images_dir, name)
                os.rename(file_path, name_file_new)
        except:
            # Hubo un error de carga
            return render_template("center/new.html", error=True)
        form = request.form
        Center.create(
            Center(
                name=form["name"],
                address=request.form["address"],
                phone=form["phone"],
                opens=datetime.datetime.strptime(
                    form["opens"], "%H:%M"
                ).time(),
                closes=datetime.datetime.strptime(
                    form["closes"], "%H:%M"
                ).time(),
                town=form["town_id"],
                web=form["web"],
                email=form["email"],
                protocol=name,
                longitude=form["lng"],
                latitude=form["lat"],
                state=CenterState.find_by_name("Aprobado"),
                center_type=CenterType.find_by_name(form["center_type"]),
            )
        )
        return redirect(url_for("center_index"))


def __crearFormulario(
    nombre,
    direccion,
    telefono,
    hora_apertura,
    hora_cierre,
    municipio,
    pagina,
    correo,
    protocolo,
    lng,
    lat,
    tipo,
    tipos_de_centros,
):
    class Form:
        name = nombre
        address = direccion
        phone = telefono
        opens = str(hora_apertura)
        closes = str(hora_cierre)
        town = municipio
        web = pagina
        email = correo
        protocol = protocolo
        longitude = str(lng)
        latitude = str(lat)
        center_type = tipo
        center_types = tipos_de_centros

    return Form()


def new():
    """
    Genera el formulario para creacion de centros.
    - Aborta si no hay usuario autenticado y si el usuario de la sesion
    no tiene permisos para crear centros.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "center_new"):
        abort(401)

    all_center_types = CenterType.get_all()
    aux_center_types = []
    for center_type in all_center_types:
        aux_center_types.append(center_type.name)

    form = __crearFormulario(
        "",
        "",
        "",
        "08:00",
        "16:00",
        0,
        "",
        "",
        "",
        "",
        "",
        0,
        aux_center_types,
    )
    return render_template("center/new.html", form=form)


def edit():
    """
    Se encarga de la edicion de centros.
    - Aborta si no hay usuario autenticado, si no hay id en argumentos,
    si no existe centro con la id pasada y si el usuario de la
    sesión no tiene permisos para editar usuarios.
    - En GET rellena los datos del form con los datos del centro
    pasado.
    - En POST valida los datos del form: si valida updatea el centro
    en la base de datos. En caso contrario recarga con los datos
    anteriores e informa errores.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "center_edit"):
        abort(401)
    center_id = request.args.get("id")
    if not center_id:
        abort(404)
    center = Center.find_by_id(center_id)
    if not center:
        abort(404)

    all_center_types = CenterType.get_all()
    aux_center_types = []
    for center_type in all_center_types:
        aux_center_types.append(center_type.name)

    class Form:
        name = center.name
        address = center.address
        phone = center.phone
        opens = str(center.opens)
        closes = str(center.closes)
        town = center.town
        web = center.web
        email = center.email
        protocol = center.protocol
        longitude = str(center.longitude)
        latitude = str(center.latitude)
        state = center.center_state_id
        center_type = str(CenterType.find_by_id(center.center_type_id).name)
        center_types = aux_center_types

    formDatosViejos = Form()

    if request.method == "GET":
        return render_template("center/edit.html", form=formDatosViejos)
    if request.method == "POST":
        form_validate = CenterForm()

        filename = request.files["archivo"].filename
        form_validate.llenarDatos(request.form, filename)
        form = request.form
        if not (form_validate.validate()):
            form = __crearFormulario(
                form["name"],
                form["address"],
                form["phone"],
                form["opens"],
                form["closes"],
                form["town_id"],
                form["web"],
                form["email"],
                "",
                form["lng"],
                form["lat"],
                form["center_type"],
                aux_center_types,
            )
            return render_template(
                "center/edit.html", form_validate=form_validate, form=form
            )

        try:
            name_file_new = ""
            file = request.files["archivo"]
            name_file_new = ""
            if file.filename != "":
                filename = secure_filename(file.filename)
                images_dir = current_app.config["UPLOAD_PROTOCOL_DEST"]
                os.makedirs(images_dir, exist_ok=True)
                file_path = os.path.join(images_dir, filename)
                file.save(file_path)
                name = str(uuid.uuid4()) + ".pdf"
                while os.path.exists(name):
                    name = str(uuid.uuid4()) + ".pdf"
                name_file_new = os.path.join(images_dir, name)
                os.rename(file_path, name_file_new)
                # borro el archivo anterior
                if center.protocol != "":
                    pdf_dir = current_app.config["UPLOAD_PROTOCOL_DEST"]
                    ruta = os.path.join(pdf_dir, center.protocol)
                    os.remove(ruta)
                # update centro
                center_protocol = name
            else:
                center_protocol = center.protocol
        except:
            # Hubo un error de carga
            return render_template(
                "center/edit.html", form=formDatosViejos, error=True
            )
        form = request.form
        center = Center.update_center_by_id(
            center_id,
            name=form["name"],
            email=form["email"],
            address=form["address"],
            phone=form["phone"],
            opens=datetime.datetime.strptime(form["opens"], "%H:%M:%S").time(),
            closes=datetime.datetime.strptime(
                form["closes"], "%H:%M:%S"
            ).time(),
            town=int(form["town_id"]),
            web=form["web"],
            protocol=center_protocol,
            longitude=form["lng"],
            latitude=form["lat"],
            center_type=CenterType.find_by_name(form["center_type"]).id,
        )
    return redirect(url_for("center_index"))


def delete():
    """
    Se encarga borrar usuarios del sistema.
    - Aborta si no hay usuario autenticado, si no hay id en argumentos,
    si no existe centro con la id pasada y si el usuario de la sesion
    no tiene permisos para bloquear/desbloquear usuarios.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "center_delete"):
        abort(401)
    form = CenterDeleteForm(request.form)
    center_id = int(form.center_id.data)
    if not center_id:
        abort(404)
    center_id = int(form.center_id.data)
    center = Center.find_by_id(center_id)
    if not center:
        abort(404)
    if form.validate():
        delete_turns(center)
        Center.delete(center)
    return redirect(url_for("center_index"))


def certify(form):
    """
    Se encarga de los permisos para la aceptación
    o rechazo de un centro.
    - Aborta si el usuario no está autenticado.
    - Aborta si el usuario no tiene permiso.
    - Aborta si el centro no exise.
    """
    user_email = authenticated(session)
    if not user_email:
        abort(401)
    if not check_permission(user_email, "center_certify"):
        abort(401)
    center_id = int(form.center_id.data)
    if not center_id:
        abort(404)
    center = Center.find_by_id(center_id)
    if not center:
        abort(404)
    return center


def accept():
    """ Se encarga del formulario de aceptación de un centro """
    form = CenterCertifyForm(request.form)
    center = certify(form)
    if form.validate():
        center.accept()
    return redirect(url_for("center_index"))


def reject():
    """ Se encarga del formulario de rechazo de un centro """
    form = CenterCertifyForm(request.form)
    center = certify(form)
    if form.validate():
        center.reject()
    return redirect(url_for("center_index"))
