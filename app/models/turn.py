from app.db import db
import app.helpers.crud as crud
from datetime import date, timedelta
from app.models.center import Center


class Turn(db.Model):
    """
    Una clase que representa los turnos que una persona puede sacar
    para cada centro de donaciones.

    Attributes:
        __tablename__ (string): Nombre de la tabla en la base de datos
            con la cual se relaciona el modelo.
        id (int): Identificador del turno en la base de datos.
        email (string): Correo electrónico de la persona que sacó el
            turno.
        day (date): Fecha para la que el turno tiene validez.
        center_id (int): Id del centro para el cual se sacó el turno.
        schedule_id (int): Id del horario durante el cual tiene validez.
    """

    __tablename__ = "turn"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45), unique=False, nullable=False)
    day = db.Column(db.Date, unique=False, nullable=False)
    center_id = db.Column(
        db.Integer, db.ForeignKey("center.id"), nullable=False
    )
    schedule_id = db.Column(
        db.Integer, db.ForeignKey("schedule.id"), nullable=False
    )

    def __init__(self, email=None, day=None, center=None, schedule=None):
        """
        Constructor de turnos.

        Args:
            email (string): Una dirección de correo.
            day (Date): Una fecha.
            center (Center): Un centro de donaciones.
            schedule (Schedule): Un horario.
        """
        self.email = email
        self.day = day
        self.center = center
        self.schedule = schedule

    @classmethod
    def create(cls, turn):
        """
        Agrega un turno a la base de datos.

        Args:
            turn (Turn): Una instancia de la clase Turn.

        Returns:
            turn: El turno creado.
        """
        return crud.create(turn)

    @classmethod
    def delete(cls, turn):
        """
        Borra un turno de la base de datos.

        Args:
           turn (Turn): Una instancia de la clase Turn.
        """
        crud.delete(turn)

    @classmethod
    def get_all(cls):
        """
        Busca todos los turnos de la base de datos.

        Returns:
            turn: Una lista de todos los turnos de la base de datos.
        """
        return cls.query.all()

    def has_day_and_schedule(self, day, schedule):
        """
        Retorna true si el turno posee el dia y el bloque horario
        pasados.

        Args:
            day (date): La fecha de un dia.
            schedule (schedule): Un bloque horario.

        Returns:
            bool: True si dia y bloque horario son iguales,
                False en caso contrario.
        """
        return (self.day == day) and (self.schedule == schedule)

    def has_day(self, day):
        """
        Retorna true si el turno pertenece al dia pasado.

        Args:
            day (date): La fecha de un dia.

        Returns:
            bool: True si el turno posee ese día.
        """
        return self.day == day

    @classmethod
    def find_by_id(cls, asked_id):
        """
        Retorna un centro por su id.

        Args:
            asked_id (int): La id de un centro.

        Returns:
            center: Un centro.
        """
        return cls.query.filter_by(id=asked_id).first()

    @classmethod
    def paginated_turns_from(cls, id, items, page):
        """
        Retorna todos los turnos paginados de un centro
        especifico.

        Args:
            id (int): La id de un centro.
            items (int): Cantidad de objetos por página.
            page (int): Número de página.

        Returns:
            list(turn): Lista de turnos.
        """
        return (
            cls.query.order_by(cls.day, cls.schedule_id)
            .filter(cls.center_id == id)
            .paginate(page, items)
        )

    @classmethod
    def search_by_center(cls, page, items, c_name):
        """
        Retorna los turnos que pertenezcan a un centro que
        en su nombre contenga el string c_name.

        Args:
            page (int): Número de página.
            items (int): Cantidad de objetos por página.
            c_name (string): Nombre de búsqueda.

        Returns:
            list(turn): Lista de turnos.
        """
        days = [
            date.today(),
            date.today() + timedelta(days=1),
            date.today() + timedelta(days=2),
        ]
        centers = Center.centers_with_name(c_name)
        ids = []
        for center in centers:
            ids.append(center.id)
        return (
            cls.query.order_by(cls.day, cls.schedule_id)
            .filter(cls.center_id.in_(ids))
            .filter(cls.day.in_(days))
            .paginate(page, items)
        )

    @classmethod
    def search_by_email(cls, page, items, email):
        """
        Retorna los turnos que contienen un email que
        contenga lo que se recibe como string.

        Args:
            page (int): Número de página.
            items (int): Cantidad de objetos por página.
            email (string): Email a buscar.

        Returns:
            list(turn): Lista de turnos.
        """
        days = [
            date.today(),
            date.today() + timedelta(days=1),
            date.today() + timedelta(days=2),
        ]
        return (
            cls.query.order_by(cls.day, cls.schedule_id)
            .filter(cls.email.contains(email), cls.day.in_(days))
            .paginate(page, items)
        )

    @classmethod
    def search_by_email_and_center(cls, page, items, email, c_name):
        """
        Retorna los turnos que pertenezcan a un centro que
        en su nombre contenga el string c_name y que en su
        email contenga el string email.

        Args:
            page (int): Número de página.
            items (int): Cantidad de objetos por página.
            email (string): Email a buscar.
            c_name (string): Nombre de búsqueda.

        Returns:
            list(turn): Lista de turnos.
        """
        days = [
            date.today(),
            date.today() + timedelta(days=1),
            date.today() + timedelta(days=2),
        ]
        centers = Center.centers_with_name(c_name)
        ids = []
        for center in centers:
            ids.append(center.id)
        return (
            cls.query.order_by(cls.day, cls.schedule_id)
            .filter(cls.email.contains(email))
            .filter(cls.center_id.in_(ids))
            .filter(cls.day.in_(days))
            .paginate(page, items)
        )

    @classmethod
    def paginated_turns(cls, page, items):
        """
        Retorna una lista de turnos paginada.

        Args:
            page (int): Número de página.
            items (int): Cantidad de objetos por página.

        Returns:
            list(turn): Lista de turnos.
        """
        days = [
            date.today(),
            date.today() + timedelta(days=1),
            date.today() + timedelta(days=2),
        ]
        return (
            cls.query.order_by(cls.day, cls.schedule_id)
            .filter(cls.day.in_(days))
            .paginate(page, items)
        )
