import datetime
from passlib.hash import sha256_crypt
from app.db import db
import app.helpers.crud as crud
from app.models.role import Role

users_have_roles = db.Table(
    "users_have_roles",
    db.Column(
        "user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True
    ),
    db.Column(
        "role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True
    ),
)


class User(db.Model):
    """
    Una clase que representa a un usuario.

    Attributes:
        __tablename__ (string): Nombre de la tabla de la base de datos
            con la cual se relaciona el modelo.
        id (int): Identificador del usuario en la base de datos.
        email (string): Correo electrónico del usuario.
        username (string): Nombre representativo del usuario.
        password (string): Contraseña del usuario.
        active (bool): ¿El usuario está activo?.
        update_at (DateTime): Representa el momento en el que el
            usuario se actualizó por última vez.
        created_at (DateTime): Representa el momento en el que el
            usuario se creó.
        first_name (string): Nombre de pila del usuario.
        last_name (string): Apellido del usuario.
        roles (list(Role)): Lista de roles que posee el usuario.
    """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    roles = db.relationship(
        "Role",
        secondary=users_have_roles,
        backref=db.backref("users", lazy=True),
    )

    def __init__(
        self,
        email=None,
        username=None,
        password=None,
        first_name=None,
        last_name=None,
        active=None,
    ):
        """
        Constructor para usuarios.

        Args:
            email (string): Un email.
            username (string): Un nombre de usuario.
            password (string): Una password.
            first_name (string): Un nombre.
            last_name (string): Un apellido.
            active (bool): ¿El usuario está activo?
        """
        self.email = email
        self.username = username
        self.password = sha256_crypt.encrypt(password)
        self.active = active
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    @classmethod
    def create(cls, user):
        """
        Agrega usuario a la base de datos.

        Args:
            user (user): Una instancia de la clase User.
        """
        return crud.create(user)

    @classmethod
    def delete(cls, user):
        """
        Elimina usuario de la base de datos.

        Args:
            user (user): Una instancia de la clase User.
        """
        crud.delete(user)

    @classmethod
    def update_user_by_id(
        cls, id, email, password, first_name, last_name, username
    ):
        """
        Busca un usuario por su id y lo actualiza en la base de datos
        con los datos recibidos. Si recibe una contraseña nula, no la
        actualiza.

        Args:
            id (int): El identificador del usuario a actualizar.
            email (string): Un email.
            password (string): Una password.
            first_name (string): Un nombre.
            last_name (string): Un apellido.
            username (string): Un nombre de usuario.
        """
        user = cls.find_by_id(id)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.updated_at = datetime.datetime.now()

        if password:
            user.password = sha256_crypt.encrypt(password)

        db.session.commit()

    @classmethod
    def find_by_email_and_pass(cls, email, password):
        """
        Busca un usuario en el cual coincidan email y password
        y si existe lo devuelve.

        Args:
            email (string): Un email.
            password (string): Una password.

        Returns:
            user: Un usuario.
        """
        return cls.query.filter(
            cls.email == email and cls.password == password
        ).first()

    @classmethod
    def find_by_email(cls, asked_email):
        """
        Busca un usuario por email y si existe lo devuelve.

        Args:
            asked_email (string): Un email.

        Returns:
            user: Un usuario.
        """
        return cls.query.filter_by(email=asked_email).first()

    @classmethod
    def find_by_username(cls, asked_username):
        """
        Busca un usuario por username y si existe lo devuelve.

        Args:
            asked_username (string): Un username.

        Returns:
            user: Un usuario.
        """
        return cls.query.filter_by(username=asked_username).first()

    @classmethod
    def find_by_id(cls, asked_id):
        """
        Busca un usuario por id y si existe lo devuelve.

        Args:
            asked_id (int): Un id.

        Returns:
            user: Un usuario.
        """
        return cls.query.filter_by(id=asked_id).first()

    @classmethod
    def search_by_username(cls, page, limit, substring):
        """
        Busca usuarios que contengan un substring en su nombre de
        usuario. Luego los pagina y devuelve la página pedida.

        Args:
            substring (string): Un substring que debe estar en el
                nombre de usuario.
            limit (int): Cantidad máxima de usuarios a devolver.
            page (int): Tanda de usuarios a devolver.

        Returns:
            users: Usuarios que tienen el substring en su
                username, guardados en un objeto 'Pagination', con
                cantidad máxima 'limit' y offset 'page' * 'limit'.
        """
        return (
            cls.query.order_by(cls.username)
            .filter(cls.username.contains(substring))
            .paginate(page, limit)
        )

    @classmethod
    def search_by_username_and_state(
        cls, page, limit, username="", active=True
    ):
        """
        Busca usuarios que contengan un substring en su nombre de
        usuario, que esten activos o no. Luego los pagina y devuelve la
        página pedida.

        Args:
            substring (string): Un substring que debe estar en el
            nombre de usuario.
            active (boolean): Booleano que determina si se buscan
                usuarios activos o bloqueados.
            limit (int): Cantidad máxima de usuarios a devolver.
            page (int): Tanda de usuarios a devolver.

        Returns:
            users: Usuarios que tienen el substring en su username, y
            que estan activos/bloqueados, guardados en un objeto
            'Pagination' con cantidad máxima 'limit' y offset
            'page' * 'limit'.
        """
        return (
            cls.query.order_by(cls.username)
            .filter(cls.username.contains(username), cls.active == active)
            .paginate(page, limit)
        )

    @classmethod
    def paginate(cls, page, limit):
        """
        Pagina a todos los usuarios y devuelve la página pedida.

        Args:
            limit (int): Cantidad máxima de usuarios a devolver.
            page (int): Tanda de usuarios a devolver.

        Returns:
            users: Un objeto 'Pagination' con todos los usuarios.
        """
        return cls.query.paginate(page, limit)

    @classmethod
    def all(cls):
        """
        Devuelve todos los usuarios.

        Returns:
            list: Una lista con todos los usuarios.
        """
        return User.query.order_by(cls.username).all()

    @classmethod
    def assign_role_to(cls, user_id, new_role):
        """
        Carga un rol en la lista de roles de un usuario.

        Args:
            user_id (int): La Id del usuario al que se le cargará
                un rol.
            new_role (int): La Id del rol que se quiere cargar.
        """
        user = User.find_by_id(user_id)
        role = Role.find_by_id(new_role)
        user.roles.append(role)
        db.session.commit()

    @classmethod
    def has_all_roles(cls, user):
        """
        Retorna verdadero si un usuario tiene todos los roles que
        hay en el sistema.

        Args:
            user (user): El usuario sobre el cual se quiere preguntar.

        Returns:
            bool: Retorna true si tiene todos los roles, en caso
                contrario retorna false.
        """
        roles = Role.get_all()
        return len(roles) == len(user.roles)

    def user_has_role(self, role_name):
        """
        Retorna verdadero si un usuario tiene el rol buscado.

        Args:
            role_name (string): Nombre del rol.

        Returns:
            bool: Retorna true si tiene el rol, en caso
                contrario retorna false.
        """
        rol = Role.find_by_name(role_name)
        return rol in self.roles

    def user_has_permission(self, permission_name):
        """
        Retorna verdadero si un usuario tiene el permiso buscado.

        Args:
            role_permission (string): Nombre del permiso.

        Returns:
            bool: Retorna true si tiene el permiso, en caso
                contrario retorna false.
        """
        for rol in self.roles:
            if rol.find_permission(permission_name):
                return True
        return False

    def remove_role(self, role):
        """
        Se encarga de borrar un rol de la lista de roles de un usuario.

        Args:
            role (role): El rol a borrar del listado.
        """
        if role in self.roles:
            self.roles.remove(role)
        db.session.commit()

    def is_my_password(self, password):
        """
        Verifica que el string recibido sea el mismo que generó el hash
            guardado en la base de datos.

        Args:
            password (string): Contraseña a comparar con la del
                usuario.

        Returns:
            bool: Un booleano que confirma si la contraseña
                recibida pertenece al usuario.
        """
        return sha256_crypt.verify(password, self.password)

    def is_active(self):
        """
        Retorna si el usuario está activo.

        Returns:
            bool: Un bool que muestra si el usuario está activo.
        """
        return self.active

    def change_state(self):
        """
        Cambia el estado de un usuario, de activo a bloqueado y viceversa.
        """
        self.active = not self.active
        db.session.commit()

    @classmethod
    def has_permission(cls, user_email, permission):
        """
        Busca un permiso dentro de los roles de un usuario.

        Args:
            user_email (string): El email del usuario a consultar.
            permission (string): El nombre del permiso a buscar.

        Returns:
            bool: Retorna verdadero si en sus roles se encuentra el
                permiso buscado.
        """
        user = User.find_by_email(user_email)
        roles = user.roles
        for rol in roles:
            if rol.find_permission(permission):
                return True
        return False

    @classmethod
    def has_role(cls, user_email, asked_rol):
        """
        Busca un rol dentro de los roles de un usuario.

        Args:
            user_email (string): El email del usuario a consultar.
            asked_rol (string): El nombre del rol buscado.

        Returns:
            bool: Retorna true si el usuario posee el rol, falso en
                caso contrario.
        """
        user = User.find_by_email(user_email)
        rol = Role.find_by_name(asked_rol)
        return rol in user.roles
