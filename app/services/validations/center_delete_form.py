from wtforms import HiddenField
from app.services.validations.csrf_base_form import CsrfBaseForm


class CenterDeleteForm(CsrfBaseForm):
    """
    Clase para generar formulario para borrar un usuario.
    Hereda funcionalidades y atributos de CsrfBaseForm.

    Attributes:
        user_id (HiddenField): Campo oculto que contiene
            la Id del usuario a borrar.

    """

    center_id = HiddenField()
