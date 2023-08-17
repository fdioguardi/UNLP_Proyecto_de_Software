from app.db import db
import app.helpers.crud as crud


class Configuration(db.Model):
    """
    Una clase que representa la configuracón del sistema.

    Attributes:
        __tablename__ (string): Nombre de la table en la base de datos
            con la cual se relaciona el modelo.
        id (int): Identificador de la configuración en la base de datos.
        title (string): Título de la página principal.
        description (string): Descripción de la página principal.
        email (string): Correo electrónico de contacto.
        itemsPerPage (int): Cantidad de elementos para mostrar en los
            listados del sistema.
        enable (bool): ¿Esta la página activa?
    """

    __tablename__ = "configuration"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    itemsPerPage = db.Column(db.Integer, nullable=False)
    enable = db.Column(db.Boolean, nullable=False)

    def __init__(
        self,
        title=None,
        description=None,
        email=None,
        itemsPerPage=None,
        enable=None,
    ):
        """
        Constructor para configuracion.

        Args:
            title (string): Un titulo.
            description (string): Una descripcion.
            email (string): Un email de contacto.
            itemsPerPage (integer): Un numero indicando la cantidad de.
                elementos por pagina.
            enable (bool): ¿La página está habilitada?.
        """
        self.title = title
        self.description = description
        self.email = email
        self.itemsPerPage = itemsPerPage
        self.enable = enable

    @classmethod
    def create(cls, configuration):
        """
        Agrega configuracion a la base de datos.

        Args:
            configuration (configuration): Una instancia de la clase
                Configuration.
        """
        return crud.create(configuration)

    @classmethod
    def modificar(cls, titulo, descripcion, email, cant_elementos, habilitado):
        """
        Modifica configuracion de la base de datos.

        Args:
            titulo (string): Nuevo titulo.
            descripcion (string): Nueva descripcion.
            email (string): Nuevo email de contacto.
            cant_elementos (integer): Nueva cantidad de elementos
                por pagina.
            habilitado (bool): Nuevo valor que indica si el sitio
                esta habilitado.
        """
        config = cls.getConfig()
        config.title = titulo
        config.description = descripcion
        config.email = email
        config.itemsPerPage = cant_elementos
        config.enable = habilitado
        db.session.commit()

    @classmethod
    def getConfig(cls):
        """
        Busca el objeto configuration en la base de datos.

        Returns:
            Configuration: El objeto configuration.
        """
        return cls.query.first()

    @classmethod
    def is_enabled(cls):
        """
        Informa si la pagina esta habilitada.

        Returns:
            bool: Un booleano que indica si la pagina esta habilitada.
        """
        return cls.getConfig().enable

    @classmethod
    def items_per_page(cls):
        """
        Devuelve la cantidad de elementos que debe haber por página
        en los listados del sistema.

        Returns:
            number: Un número que representa la cantidad de elementos
                por página del listado.
        """
        return cls.getConfig().itemsPerPage
