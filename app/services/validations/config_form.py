from wtforms import StringField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Email
from app.services.validations.csrf_base_form import CsrfBaseForm


class ConfigForm(CsrfBaseForm):
    """
    Clase para generar y validar formulario de configuracion de pagina.

    Attributes:
        titulo (StringField): Campo de string para el titulo.
        descripcion (TextAreaField): Campo de texto para la descripcion.
        email (StringField): Campo de string para el email.
        cantElement (IntegerField): Campo de integer para cantElement
        (indica la cantidad de elementos por pagina).
        habilitado(BooleanField): Campo de boolean para habilitado
        (indica si la pagina esta habilitada)

    """

    titulo = StringField(
        "Titulo",
        [DataRequired(message="Por favor ingrese un titulo.")],
        render_kw={"class": "form-control"},
    )
    descripcion = TextAreaField(
        "Descripcion",
        [DataRequired(message="Por favor ingrese una descripcion.")],
        render_kw={"class": "form-control"},
    )
    email = StringField(
        "Correo electrónico",
        [
            DataRequired(message="Por favor ingrese un correo electrónico."),
            Email(message="El correo electrónico ingresado no es válido."),
        ],
        render_kw={
            "placeholder": "ejemplo@coldmail.com",
            "class": "form-control",
        },
    )
    cantElement = IntegerField(
        "Cantidad de elementos por pagina",
        [
            DataRequired(message="Por favor ingrese un numero."),
            NumberRange(message="Ingrese un número mayor que cero.", min=1),
        ],
        render_kw={"class": "form-control"},
    )
    habilitado = BooleanField("Habilitar sitio")

    def completarDatos(self, config):
        """
        Carga los datos del formulario con los datos de la
        configuracion ingresados

        Args:
            config (Configuration): Una instancia de la
                clase Configuration
        """
        self.titulo.data = config.title
        self.descripcion.data = config.description
        self.email.data = config.email
        self.cantElement.data = config.itemsPerPage
        self.habilitado.data = config.enable
