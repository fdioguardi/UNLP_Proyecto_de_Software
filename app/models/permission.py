from app.db import db
import app.helpers.crud as crud


class Permission(db.Model):
    """
    Una clase que representa a un permiso para realizar una acción.

    Attributes:
        __tablename__ (string): Nombre de la table en la base de datos
            con la cual se relaciona el modelo.
        id (int): Identificador del permiso en la base de datos
        name (string): Nombre del permiso.
    """

    __tablename__ = "permission"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, name=None):
        """
        Constructor para permisos.

        Args:
            name (string): Un nombre.
        """
        self.name = name

    @classmethod
    def create(cls, permission):
        """
        Agrega un permiso a la base de datos.

        Args:
            permission (Permission): Una instancia de la
                clase Permission.
        """
        return crud.create(permission)

    @classmethod
    def delete(cls, permission):
        """
        Borra un permiso de la base de datos.

        Args:
            permission (Permission): Una instancia de la
                clase Permission.
        """
        crud.delete(permission)

    @classmethod
    def find_by_name(cls, a_name):
        """
        Busca un permiso por nombre y si existe lo devuelve.

        Args:
            a_name (string): Un nombre.

        Returns:
            permission: Un permiso.
        """
        return cls.query.filter_by(name=a_name)
