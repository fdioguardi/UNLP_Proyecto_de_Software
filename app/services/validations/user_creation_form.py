from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models.user import User
from app.services.validations.csrf_base_form import CsrfBaseForm


class UserCreationForm(CsrfBaseForm):
    """
    Clase para generar y validar formulario de inicio de sesion
    de usuarios

    Attributes:
        first_name (StringField): Campo de string para el nombre.
        last_name (StringField): Campo de string para el apellido.
        email (StringField): Campo de string para el email.
        password (PasswordField): Campo de password para la password.
        username (StringField): Campo de string para el username.
        active (BooleanField): Campo booleano para determinar si usuario
        esta activo.
    """

    first_name = StringField(
        "Nombre",
        [DataRequired(message="Por favor ingrese su nombre.")],
        render_kw={"placeholder": "Juan", "class": "form-control"},
    )
    last_name = StringField(
        "Apellido",
        [DataRequired(message="Por favor ingrese su apellido.")],
        render_kw={"placeholder": "Perez", "class": "form-control"},
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
    password = PasswordField(
        "Contraseña",
        [DataRequired(message="Por favor ingrese una contraseña.")],
        render_kw={"placeholder": "contraseña", "class": "form-control"},
    )
    username = StringField(
        "Nombre de usuario",
        [DataRequired(message="Por favor ingrese un nombre de usuario.")],
        render_kw={"placeholder": "ejemplo", "class": "form-control"},
    )
    active = BooleanField("Activar usuario")

    def validate_email(form, field):
        """
        Valida que el email ingresado no este en uso.

        Parameters:
            form (Form): Un formulario.
            field (StringField): Un StringField con un email.
        Raises:
            ValidationError: si el email ingresado esta en uso.
        """
        if User.find_by_email(field.data):
            raise ValidationError(
                "El correo electrónico ingresado ya está en uso."
            )

    def validate_username(form, field):
        """
        Valida que el email ingresado no este en uso.

        Parameters:
            form (Form): Un formulario.
            field (StringField): Un StringField con un username.
        Raises:
            ValidationError: si el username esta en uso.
        """
        if User.find_by_username(field.data):
            raise ValidationError(
                "El nombre de usuario ingresado ya está en uso."
            )
