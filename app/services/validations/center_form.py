from wtforms import StringField
from wtforms.validators import DataRequired, Email, ValidationError
from app.helpers.regex import validate_email, validate_telephone, validate_time
from wtforms import Form


class CenterForm(Form):
    name = StringField(
        DataRequired(message="Por favor ingrese el nombre del centro.")
    )
    address = StringField(
        DataRequired(message="Por favor seleccione una dirección.")
    )
    phone = StringField(
        DataRequired(message="Por favor ingrese un número de teléfono.")
    )
    opens = StringField(
        DataRequired(message="Por favor ingrese un horario de apertura")
    )
    closes = StringField(
        DataRequired(message="Por favor, ingrese un horario de cierre")
    )
    town = StringField(
        DataRequired(message="Por favor, seleccione un municipio")
    )
    web = StringField()
    email = StringField(
        Email(message="El correo electrónico ingresado no es válido.")
    )
    protocol = StringField()
    longitude = StringField(
        DataRequired(message="Por favor seleccione una dirección.")
    )  # ver como se pone mas adelante
    latitude = StringField(
        DataRequired(message="Por favor seleccione una dirección.")
    )  # ver como se pone mas adelante
    center_type = StringField(
        DataRequired(message="Por favor seleccione un tipo de centro.")
    )

    def llenarDatos(self, form, filename):
        """
        Completa los datos del formulario.

        Args:
            form (Form): Un formulario.
            filename (string): Nombre del pdf.
        """
        self.name.data = form["name"]
        self.address.data = form["address"]
        self.phone.data = form["phone"]
        self.opens.data = form["opens"]
        self.closes.data = form["closes"]
        self.town.data = form["town_id"]
        self.web.data = form["web"]
        self.email.data = form["email"]
        self.protocol.data = filename
        self.longitude.data = form["lng"]
        self.latitude.data = form["lat"]
        self.center_type.data = form["center_type"]

    def validate_name(form, field):
        """
        Valida que el nombre ingresado no sea vacío.

        Args:
            form (Form): Un formulario.
            field (StringField): Un StringField con un nombre.

        Raises:
            ValidationError: si el nombre esta vacío.
        """
        if field.data.strip() == "":
            raise ValidationError("Por favor ingrese el nombre del centro.")

    def validate_address(form, field):
        """
        Valida que la dirección ingresado no sea vacío.

        Args:
            form (Form): Un formulario.
            field (StringField): Un StringField con una dirección.

        Raises:
            ValidationError: si la dirección esta vacío.
        """
        if field.data == "":
            raise ValidationError("Por favor seleccione una dirección.")

    def validate_phone(form, field):
        """
        Valida que el teléfono ingresado no sea vacío.

        Args:
            form (Form): Un formulario.
            field (StringField): Un StringField con un teléfono.

        Raises:
            ValidationError: si el teléfono esta vacío.
        """

        if not (validate_telephone(field.data)):
            raise ValidationError("Por favor ingrese un teléfono válido.")
        if field.data == "":
            raise ValidationError("Por favor ingrese un numero de teléfono.")

    def validate_opens(form, field):
        """
        Valida que el horario de apuertura ingresado no sea vacío.

        Args:
            form (Form): Un formulario.
            field (StringField): Un StringField con un horario de
                apuertura.

        Raises:
            ValidationError: si el horario de apuertura esta vacío.
        """
        hora = field.data[0:5]
        if not (validate_time(hora)):
            raise ValidationError("Por favor ingrese un horario válido")
        if field.data == "":
            raise ValidationError(
                "Por favor seleccione un horario de apertura."
            )

    def validate_closes(form, field):
        """
        Valida que el horario de cierre ingresado no sea vacío.

        Args:
            form (Form): Un formulario.
            field (StringField): Un StringField con un horario de
                cierre.

        Raises:
            ValidationError: si el horario de cierre esta vacío.
        """
        hora = field.data[0:5]
        if not (validate_time(hora)):
            raise ValidationError("Por favor ingrese un horario válido")
        if field.data == "":
            raise ValidationError("Por favor seleccione un horario de cierre.")

    def validate_town(form, field):
        """
        Valida que el municipio ingresado no sea vacío.

        Args:
            form (Form): Un formulario.
            field (StringField): Un StringField con un municipio.

        Raises:
            ValidationError: si el municipio esta vacío.
        """
        if field.data == "":
            raise ValidationError("Por favor seleccione un municipio.")

    def validate_email(form, field):
        """
        Valida que el email ingresado no sea vacío.

        Args:
            form (Form): Un formulario.
            field (StringField): Un StringField con un email.

        Raises:
            ValidationError: si el email esta vacío.
        """
        if field.data != "":
            if not (validate_email(field.data)):
                raise ValidationError("Por favor ingrese un email válido.")

    def validate_longitude(form, field):
        """
        Valida que la longitud ingresada no sea vacía.

        Args:
            form (Form): Un formulario.
            field (StringField): Un StringField con una longitud.

        Raises:
            ValidationError: si la longitud esta vacía.
        """
        if form.address.data != "":
            try:
                float(field.data)
            except:
                raise ValidationError(
                    "Por favor selecciona una direccion valida."
                )

            if field.data == "":
                raise ValidationError("Por favor seleccione una direccion.")

    def validate_latitude(form, field):
        """
        Valida que la latitud ingresada no sea vacía.

        Args:
            form (Form): Un formulario.
            field (StringField): Un StringField con una latitud.

        Raises:
            ValidationError: si la latitud esta vacía.
        """
        if form.address.data != "":
            try:
                float(field.data)
            except:
                raise ValidationError(
                    "Por favor seleccione una dirección valida."
                )
            if field.data == "":
                raise ValidationError("Por favor seleccione una dirección.")

    def validate_center_type(form, field):
        """
        Valida que el tipo de centro ingresado no sea vacío.

        Args:
            form (Form): Un formulario.
            field (StringField): Un StringField con un tipo de centro.

        Raises:
            ValidationError: si el tipo de centro esta vacío.
        """
        if field.data == "":
            raise ValidationError("Por favor seleccione un tipo de centro.")

    def validate_protocol(form, field):
        """
        Valida que el protocolo ingresado no sea vacío.

        Args:
            form (Form): Un formulario.
            field (StringField): Un StringField con un protocolo.

        Raises:
            ValidationError: si el protocolo esta vacío.
        """
        if field.data != "":
            aux_cadena = field.data.split(".")
            if aux_cadena[len(aux_cadena) - 1] != "pdf":
                raise ValidationError("Por favor seleccione un archivo pdf.")
