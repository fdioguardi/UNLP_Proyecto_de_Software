from wtforms import HiddenField
from app.services.validations.csrf_base_form import CsrfBaseForm


class CenterCertifyForm(CsrfBaseForm):
    """
    Clase para generar formulario para aceptar o rechazar un centro.
    Hereda funcionalidades y atributos de CsrfBaseForm.

    Attributes:
        center_id (HiddenField): Campo oculto que contiene
            la Id del centro a evaluar.
    """

    center_id = HiddenField()
