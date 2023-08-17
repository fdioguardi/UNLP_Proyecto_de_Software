from app.services.validations.csrf_base_form import CsrfBaseForm
from wtforms import HiddenField


class UserStateForm(CsrfBaseForm):
    """
    Clase para generar formulario para activar/bloquear un usuario.
    Hereda funcionalidades y atributos de CsrfBaseForm.

    Attributes:
        user_id (HiddenField): Campo oculto que contiene
            la Id del usuario a activar/bloquear.
    """

    user_id = HiddenField()
