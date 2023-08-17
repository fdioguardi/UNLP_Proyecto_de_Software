from os import environ
from flask import Flask, render_template, session
from flask_session import Session
from flask_restful import Api
from config import config
from app.db import db
from app.resources import user
from app.resources import center
from app.resources import auth
from app.helpers import handler
from app.helpers import auth as helper_auth
from dotenv import load_dotenv
from app.resources import role
from app.resources import configuration
from app.resources import mantenimiento
from app.resources.api.turn_reservation_api import TurnReservationAPI
from app.resources.api import center_turns_api
from app.resources.api import town_api
from app.resources.api.turn_list_api import TurnListAPI
from app.resources.api import center_api
from app.resources.api import center_list_api
from app.resources.api import center_type_api
from app.helpers import permission as helper_permission
from app.helpers.permission import check, is_active
from app.helpers.configuration import is_enabled
from app.helpers.role import has_role, email_has_role
from app.helpers.center import is_pending
from app.models.configuration import Configuration
from app.resources import turn
from app.models.center import Center
from flask_cors import CORS


def create_app(environment="development"):

    app = Flask(__name__)

    # Media dir
    app.config["UPLOAD_PROTOCOL_DEST"] = "app/static/uploads"

    # Configuración inicial de la app

    # Carga las variables de ambiente
    load_dotenv()

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # SQLAlchemy
    db.init_app(app)

    # Flask-RESTful
    api = Api(app)

    # Api Routes
    api.add_resource(TurnReservationAPI, "/centros/<int:id>/reserva")
    api.add_resource(TurnListAPI, "/centros/<int:id>/turnos_disponibles/")
    api.add_resource(center_list_api.CenterListApi, "/centros")
    api.add_resource(center_api.CenterApi, "/centros/<center_id>")
    api.add_resource(center_type_api.CenterTypeApi, "/tipos_de_centro")
    api.add_resource(town_api.TownApi, "/municipios")
    api.add_resource(center_turns_api.CenterTurnsApi, "/turnos_por_centro")

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(has_permission=helper_permission.check)
    app.jinja_env.globals.update(has_role=has_role)
    app.jinja_env.globals.update(email_has_role=email_has_role)
    app.jinja_env.globals.update(is_pending=is_pending)

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion",
        "auth_authenticate",
        auth.authenticate,
        methods=["POST"],
    )
    app.add_url_rule(
        "/usuarios/borrar", "user_delete", user.delete, methods=["POST"]
    )

    # CORS
    cors = CORS(app)

    # Rutas de Usuarios
    app.add_url_rule(
        "/usuarios", "user_index", user.index, methods=["GET", "POST"]
    )
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule(
        "/usuarios/nuevo", "user_create", user.create, methods=["POST"]
    )
    app.add_url_rule(
        "/usuarios/editar", "user_edit", user.edit, methods=["POST", "GET"]
    )

    app.add_url_rule(
        "/usuarios/estado", "user_state", user.state, methods=["POST"]
    )

    # Rutas de roles
    app.add_url_rule("/roles", "role_show", role.show)
    app.add_url_rule("/roles/asignar", "role_select", role.select)
    app.add_url_rule(
        "/roles/asignar", "role_assign", role.assign, methods=["POST"]
    )
    app.add_url_rule(
        "/roles/borrar", "role_delete", role.delete, methods=["POST", "GET"]
    )

    # Rutas de centro

    app.add_url_rule(
        "/centros_index", "center_index", center.index, methods=["GET", "POST"]
    )
    app.add_url_rule("/centros/nuevo", "center_new", center.new)
    app.add_url_rule(
        "/centros/nuevo", "center_create", center.create, methods=["POST"]
    )
    app.add_url_rule(
        "/centros/editar", "center_edit", center.edit, methods=["POST", "GET"]
    )
    app.add_url_rule(
        "/centros/borrar", "center_delete", center.delete, methods=["POST"]
    )
    app.add_url_rule(
        "/centros/aceptar", "center_accept", center.accept, methods=["POST"]
    )
    app.add_url_rule(
        "/centros/rechazar", "center_reject", center.reject, methods=["POST"]
    )

    # Ruta de configuration
    app.add_url_rule(
        "/configuration", "configuration_index", configuration.index
    )
    app.add_url_rule(
        "/configuration",
        "configuration_update",
        configuration.update,
        methods=["POST"],
    )

    # Rutas de Turnos
    app.add_url_rule(
        "/centros/turnos", "turn_index", turn.index, methods=["GET", "POST"]
    )
    app.add_url_rule(
        "/centros/turnos/borrar", "turn_delete", turn.delete, methods=["POST"]
    )
    app.add_url_rule(
        "/turnos", "turn_search", turn.search, methods=["GET", "POST"]
    )
    app.add_url_rule("/centros/turnos/nuevo", "turn_new", turn.new)

    # Ruta de Mantenimiento
    app.add_url_rule("/mantenimiento", "mantenimiento", mantenimiento.index)

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        """
        Muestra el home.
        Si hay un usuario logueado y está bloqueado, lo desconecta
        y le muestra una pantalla que informa acceso no autorizado.
        """
        if "user" in session:
            is_active(session["user"])
        if not is_enabled():
            return render_template("mantenimiento.html")
        config = Configuration.getConfig()
        return render_template("home.html", config=config)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    app.register_error_handler(500, handler.internal_server_error)

    cors = CORS(app, resources={r"/tipos_de_centro/*": {"origins": "*"}})
    cors = CORS(app, resources={r"/centros/*": {"origins": "*"}})
    # Retornar la instancia de app configurada
    return app
