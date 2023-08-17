from app.db import db
import app.helpers.crud as crud


class CenterState(db.Model):
    """
    Una clase que representa los distintos estados en los que se pueden
    encontrar los centros de donaciones.

    Attributes:
        __tablename__ (string): Nombre de la tabla en la base de datos
            con la cual se relaciona el modelo.
        id (int): Identificador del estado de los centros en la base de
            datos.
        name (string): Nombre del estado de los centros.
        centers (list(Center)): Centros en el estado determinado.
    """

    __tablename__ = "center_state"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    centers = db.relationship("Center", backref="center_state", lazy=True)

    def __init__(self, name=None):
        """
        Constructor para estado de centros.

        Args:
            name (string): Un nombre.
        """
        self.name = name

    @classmethod
    def create(cls, center_state):
        """
        Agrega un estado de centros a la base de datos.

        Args:
            center_state (CenterState): Una instancia de la clase
                CenterState.

        Returns:
            center_state: El estado de centros creado.
        """
        return crud.create(center_state)

    @classmethod
    def delete(cls, center_state):
        """
        Borra un estado de centros de la base de datos.

        Args:
           center_state (CenterState): Una instancia de la clase
                CenterState.
        """
        crud.delete(center_state)

    @classmethod
    def find_by_name(cls, a_name):
        """
        Busca un estado de centros por nombre.

        Args:
            a_name (string): El nombre del estado de centros a buscar.

        Returns:
            center_state: El primer estado de centros encontrado con el
                nombre buscado.
        """
        return cls.query.filter_by(name=a_name).first()

    @classmethod
    def find_by_id(cls, asked_id):
        """
        Busca un estado de centros que posea un ID determinado.

        Args:
            asked_id (int): El ID del estado de centros buscado.

        Returns:
            center_state: El primer estado de centros que posea el ID
                buscado.
        """
        return cls.query.filter_by(id=asked_id).first()

    @classmethod
    def get_all(cls):
        """
        Busca todos los estados de centros de la base de datos.

        Returns:
            center_states: Una lista de todos los estados de centros de
                la base de datos.
        """
        return cls.query.all()

    @classmethod
    def get_all_aprobados(cls):
        """
        Retorna todos los centros aprobados.

        Returns:
            centers: Una lista de todos los centros aprobados de
                la base de datos.
        """
        return cls.find_by_name("Aprobado").centers

    def paginated_centers(self, page, limit):
        """
        Pagina todos los centros del estado y devuelve la página pedida.

        Args:
            page (int): Tanda de centros a devolver.
            limit (int): Cantidad máxima de centros a devolver.

        Returns:
            centers: Un objeto 'Pagination' con todos los centros del
                estado.
        """
        return self.centers[limit * (page - 1) : limit * page]

    def has_name(self, a_name):
        """
        Compara el nombre recibido con el nombre propio del estado.

        Args:
            a_name (string): Nombre a comparar.

        Returns:
            bool: True si el estado tiene el nombre recibido, False en
                caso contrario.
        """
        return self.name == a_name
