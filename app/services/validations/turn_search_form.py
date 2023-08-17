from wtforms import StringField, SelectField
from app.services.validations.csrf_base_form import CsrfBaseForm


class TurnSearchForm(CsrfBaseForm):
    """
    Clase para generar y validar formulario para buscar usuarios.
    Hereda funcionalidades y atributos de CsrfBaseForm.

    Attributes:
        select (SelectField): Campo de seleccion para buscar usuarios
            activos, bloqueados o ambos.
        search (StringField): Campo de string para buscar en los
            nombres de usuario y filtrarlos.
    """

    select = StringField(
        "Buscar por centro", render_kw={"class": "form-control"}
    )
    search = StringField(
        "Buscar por email", render_kw={"class": "form-control"}
    )

    def add_data(self, search, select):
        self.search.data = search
        self.select.data = select
