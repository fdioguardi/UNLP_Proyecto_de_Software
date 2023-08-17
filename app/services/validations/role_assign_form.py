from wtforms import SelectField
from wtforms.validators import DataRequired
from app.services.validations.csrf_base_form import CsrfBaseForm


class RoleAssignForm(CsrfBaseForm):
    """
    Clase para generar y validar formulario para asignar un rol a un
    usuario. Hereda funcionalidades y atributos de CsrfBaseForm.

    Attributes:
        role (SelectField): Campo de selección para un rol.
    """

    role = SelectField(
        "Role",
        [DataRequired(message="Rol requerido")],
        render_kw={"class": "form-control"},
    )

    def role_choices(self, rlist):
        """
        Carga una lista de roles en las opciones que va a tener
        el SelectField.

        Args:
            rlist (List): Una lista con los roles disponibles
                para un usuario.
        """
        self.role.choices = rlist
