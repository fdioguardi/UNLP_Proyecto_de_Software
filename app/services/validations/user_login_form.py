from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models.user import User
from app.services.validations.csrf_base_form import CsrfBaseForm


class UserLoginForm(CsrfBaseForm):
    """
    Clase para generar y validar formulario de inicio de sesion
    de usuarios

    Attributes:
        email (StringField): Campo de string para el email.
        password (PasswordField): Campo de password para la password.
    """

    email = StringField(
        "Correo electrónico",
        [
            DataRequired(message="Please enter an email."),
            Email(message="Por favor ingrese un correo " "electrónico."),
        ],
        render_kw={"placeholder": "Enter email", "class": "form-control"},
    )
    password = PasswordField(
        "Contraseña",
        [DataRequired(message="Por favor ingrese una contraseña.")],
        render_kw={"placeholder": "Password", "class": "form-control"},
    )

    def validate_password(form, field):
        """
        Valida que la password ingresada pertenezca al usuario

        Parameters:
            form (Form): Un formulario.
            field (StringField): Un StringField con una password.
        Raises:
            ValidationError: si no encuentra un usuario con el correo
                electronico provisto y, si lo encuentra, si no es su
                password.
        """
        user = User.find_by_email(form.email.data)
        if (not user) or (not user.is_my_password(field.data)):
            raise ValidationError("Correo electrónico o contraseña inválidas.")
