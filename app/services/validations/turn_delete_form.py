from wtforms import HiddenField
from app.services.validations.csrf_base_form import CsrfBaseForm


class TurnDeleteForm(CsrfBaseForm):
    """
    Clase para generar formulario para borrar un turno.
    Hereda funcionalidades y atributos de CsrfBaseForm.

    Attributes:
        turn_id (HiddenField): Campo oculto que contiene
            la Id del turno a borrar.

    """

    turn_id = HiddenField()
