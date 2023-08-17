from app.db import db
import app.helpers.crud as crud
from app.models.permission import Permission


roles_have_permissions = db.Table(
    "roles_have_permissions",
    db.Column(
        "role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True
    ),
    db.Column(
        "permission_id",
        db.Integer,
        db.ForeignKey("permission.id"),
        primary_key=True,
    ),
)


class Role(db.Model):
    """
    Una clase que representa a los roles.

    Attributes:
        __tablename__ (string): Nombre de la table en la base de datos
            con la cual se relaciona el modelo.
        id (int): Identificador del rol en la base de datos.
        name (string): Nombre del rol.
        permissions (list(Permissions)): Lista de los permisos
            que posee el rol.
    """

    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    permissions = db.relationship(
        "Permission",
        secondary=roles_have_permissions,
        lazy="subquery",
        backref=db.backref("roles", lazy=True),
    )

    def __init__(self, name=None):
        """
        Constructor para roles.

        Args:
            name (string): Un nombre.
        """
        self.name = name

    @classmethod
    def create(cls, role):
        """
        Agrega un rol a la base de datos.

        Args:
            role (Role): Una instancia de la clase Role.
        """
        return crud.create(role)

    @classmethod
    def delete(cls, role):
        """
        Borra un rol de la base de datos.

        Args:
            role (Role): Una instancia de la clase Role.
        """
        crud.delete(role)

    @classmethod
    def find_by_name(cls, a_name):
        """
        Busca un rol por nombre.

        Args:
            a_name (string): El nombre del rol a buscar.
        Returns:
            role: El primero rol encontrado con el nombre buscado.
        """
        return cls.query.filter_by(name=a_name).first()

    @classmethod
    def roles_missing_for(cls, user):
        """
        Busca los roles que el usuario recibido como
        parametro no tiene asignados.

        Args:
            user (User): Una instancia del usuario sobre el que se esta
                buscando roles.
        Returns:
            roles: Una lista de los roles que el usuario no posee.
        """
        all_roles = Role.query.all()
        roles = []
        for role in all_roles:
            if role not in user.roles:
                roles.append(role)
        return roles

    @classmethod
    def find_by_id(cls, asked_id):
        """
        Busca un rol que posea determinada ID.

        Args:
            asked_id (int): La Id del rol buscado.

        Returns:
            role: El primer rol que posea la Id.
        """
        return cls.query.filter_by(id=asked_id).first()

    @classmethod
    def get_all(cls):
        """
        Busca todos los roles de la base de datos.

        Returns:
            roles: Una lista de todos los roles de la base de datos.
        """
        return cls.query.all()

    def find_permission(self, asked_permission):
        """
        Busca un permiso en los permisos que tiene el rol asignados.

        Args:
            asked_permission (string): Nombre del permiso buscado.

        Returns:
            bool: retorna verdadero si tiene el permiso buscado
                dentro de sus permisos y falso en caso contrario.
        """
        for permission in self.permissions:
            if asked_permission == permission.name:
                return True
        return False
