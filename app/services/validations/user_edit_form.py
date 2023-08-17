from wtforms import PasswordField
from wtforms.validators import ValidationError
from app.models.user import User
from app.services.validations.user_creation_form import UserCreationForm
from flask import request


class UserEditForm(UserCreationForm):
    """
    Clase para generar y validar formulario para editar un usuario.
    Hereda funcionalidades y atributos de UserCreationForm.

    Attributes:
        password (PasswordField): Campo de string para la password.
    """

    password = PasswordField(
        "Contraseña",
        render_kw={"placeholder": "contraseña", "class": "form-control"},
    )

    def complete_data(self, user):
        """
        Carga los datos del formulario con los datos del usuario
        ingresado.

        Args:
            user (User): Una instancia de la clase usuario
        """
        self.first_name.data = user.first_name
        self.last_name.data = user.last_name
        self.email.data = user.email
        self.username.data = user.username
        self.active.data = user.active

    def validate_email(form, field):
        """
        Valida que el email ingresado no este en uso excepto por el
        usuario que se esta editando.

        Parameters:
            form (Form): Un formulario.
            field (StringField): Un StringField con un email.

        Raises:
            ValidationError: si el email ingresado esta en uso por otro
                usuario que no es el que se esta editando.
        """
        user = User.find_by_email(field.data)
        id = int(request.args.get("id"))
        if (user) and ((user.id) != (id)):
            raise ValidationError(
                "El correo electrónico ingresado ya está "
                "en uso por otro usuario."
            )

    def validate_username(form, field):
        """
        Valida que el username ingresado no este en uso excepto por el
        usuario que se esta editando.

        Parameters:
            form (Form): Un formulario.
            field (StringField): Un StringField con un username.

        Raises:
            ValidationError: si el username ingresado esta en uso por
                otro usuario que no es el que se esta editando.
        """
        user = User.find_by_username(field.data)
        id = int(request.args.get("id"))
        if (user) and ((user.id) != (id)):
            raise ValidationError(
                "El nombre de usuario ingresado ya está en "
                "uso por otro usuario."
            )
