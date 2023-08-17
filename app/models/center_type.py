from app.db import db
import app.helpers.crud as crud
from app.models.center_state import CenterState


class CenterType(db.Model):
    """
    Una clase que representa los distintos tipos de centros de
    donaciones.

    Attributes:
        __tablename__ (string): Nombre de la tabla en la base de datos
            con la cual se relaciona el modelo.
        id (int): Identificador del tipo de centro en la base de datos.
        name (string): Nombre del tipo de centro.
        centers (list(Center)): Centros del tipo particular.
    """

    __tablename__ = "center_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    centers = db.relationship("Center", backref="center_type", lazy=True)

    def __init__(self, name=None):
        """
        Constructor para tipos de centros.

        Args:
            name (string): Un nombre.
        """
        self.name = name

    @classmethod
    def create(cls, center_type):
        """
        Agrega un tipo de centro a la base de datos.

        Args:
            center_type (CenterType): Una instancia de la clase
                CenterType.

        Returns:
            center_type: El tipo de centro creado.
        """
        return crud.create(center_type)

    @classmethod
    def delete(cls, center_type):
        """
        Borra un tipo centro de la base de datos.

        Args:
           center_type (CenterType): Una instancia de la clase
                CenterType.
        """
        crud.delete(center_type)

    @classmethod
    def find_by_name(cls, a_name):
        """
        Busca un tipo de centro por nombre.

        Args:
            a_name (string): El nombre del tipo de centro a buscar.

        Returns:
            center_type: El primer tipo de centro encontrado con el
                nombre buscado.
        """
        return cls.query.filter_by(name=a_name).first()

    @classmethod
    def find_by_id(cls, asked_id):
        """
        Busca un tipo de centro que posea un ID determinado.

        Args:
            asked_id (int): El ID del tipo de centro buscado.

        Returns:
            center_type: El primer tipo de centro que posea el ID
                buscado.
        """
        return cls.query.filter_by(id=asked_id).first()

    @classmethod
    def get_all(cls):
        """
        Busca todos los tipos de centro de la base de datos.

        Returns:
            center_types: Una lista de todos los tipos de centro de la
                base de datos.
        """
        return cls.query.all()

    def serialize(self):
        """
        Devuelve un diccionario representativo del tipo de centro.

        Returns:
            dictionary: Diccionario con el nombre del tipo de centro y
                la cantidad de centros que se le asocian.
        """
        centers = list(
            set(self.centers) & set(CenterState.get_all_aprobados())
        )
        return {"nombre": self.name, "cant_centros": len(centers)}

    @classmethod
    def serialized_center_types(cls):
        """
        Devuelve todos los tipos de centro serializados.

        Returns:
            center_types: Una lista de todos los tipos de centro de la
                base de datos ya serializados.
        """
        return [center_type.serialize() for center_type in cls.query.all()]
