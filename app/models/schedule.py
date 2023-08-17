from app.db import db
import app.helpers.crud as crud


class Schedule(db.Model):
    """
    Una clase que representa los bloques horarios en los que una
    persona puede sacar turno en alguno de los centros de donaciones.

    Attributes:
        __tablename__ (string): Nombre de la tabla en la base de datos
            con la cual se relaciona el modelo.
        id (int): Identificador del bloque horario en la base de datos.
        start (Time): Hora de inicio del bloque horario.
        end (Time): Hora de fin del bloque horario.
        turns (list(Turn)): Lista de todos los turnos que se sacaron
            para el horario determinado, independientemente del centro.
    """

    __tablename__ = "schedule"
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Time, unique=True, nullable=False)
    end = db.Column(db.Time, unique=True, nullable=False)
    turns = db.relationship("Turn", backref="schedule", lazy=True)

    def __init__(self, start=None, end=None):
        """
        Constructor de un bloque horario.

        Args:
            start (Time): Un horario de inicio.
            end (Time): Un horario de fin.
        """
        self.start = start
        self.end = end

    @classmethod
    def create(cls, schedule):
        """
        Agrega un bloque horario la base de datos.

        Args:
            schedule (Schedule): Una instancia de la clase Schedule.

        Returns:
            schedule: El bloque horario creado.
        """
        return crud.create(schedule)

    @classmethod
    def delete(cls, schedule):
        """
        Borra un bloque horario de la base de datos.

        Args:
           schedule (Schedule): Una instancia de la clase Schedule.
        """
        crud.delete(schedule)

    @classmethod
    def get_all(cls):
        """
        Busca todos los bloques horarios de la base de datos.

        Returns:
            schedules: Una lista de todos los bloques horarios de la
                base de datos.
        """
        return cls.query.all()

    @classmethod
    def find_by_times(cls, start, end):
        """
        Busca un bloque de horario por su hora de inicio y su hora
        de fin. Si existe lo devuelve.

        Args:
            start (time): Una hora de inicio.
            end (time): Una hora de fin.

        Returns:
            schedule: Un bloque de horario.
        """
        return cls.query.filter(cls.start == start, cls.end == end).first()

    @classmethod
    def get_unused_schedules(cls, turns):
        """
        Retorna los bloques de horarios disponibles a partir
        de una lista de turnos ocupados.

        Args:
            turns (list(Turn)): Lista de turnos.

        Returns:
            list(Schedule): Lista de bloques de horarios
                disponibles.
        """
        turnSchedules = [turn.schedule for turn in turns]
        return [
            schedule
            for schedule in cls.get_all()
            if schedule not in turnSchedules
        ]
