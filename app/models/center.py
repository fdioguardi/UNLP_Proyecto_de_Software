import functools
import itertools
from app.db import db
import app.helpers.crud as crud
from app.models.schedule import Schedule
from app.models.center_type import CenterType
from app.models.center_state import CenterState


class Center(db.Model):
    """
    Una clase que representa a los centros de donaciones.

    Attributes:
        __tablename__ (string): Nombre de la tabla en la base de datos
            con la cual se relaciona el modelo.
        id (int): Identificador del centro en la base de datos.
        name (string): Nombre del centro.
        address (string): Dirección del centro.
        phone (string): Número telefónico del centro.
        opens (time): Horario de apertura del centro.
        closes (time): Horario de cierre del centro.
        town (int): Id del municipio en el que se ubica el centro (obtenido
            mediante una API).
        web (string): Página web del centro.
        email (string): Dirección de correo electrónico del centro.
        protocol (string): Ruta al pdf que donde se detalla el protocólo
            del centro.
        longitude (string): Posición longitudinal del centro.
        latitude (string): Posición latitudinal del centro.
        center_type_id (int): Id del tipo de centro.
        center_state_id (int): Id del estado del centro.
        turns (list(Turn)): Turnos sacados para el centro.
    """

    __tablename__ = "center"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    address = db.Column(db.String(255), unique=False, nullable=False)
    phone = db.Column(db.String(15), unique=False, nullable=False)
    opens = db.Column(db.Time, unique=False, nullable=False)
    closes = db.Column(db.Time, unique=False, nullable=False)
    town = db.Column(db.Integer, unique=False, nullable=False)
    web = db.Column(db.String(255), unique=False, nullable=True)
    email = db.Column(db.String(255), unique=False, nullable=True)
    protocol = db.Column(db.String(255), unique=False, nullable=True)
    longitude = db.Column(db.String(127), unique=False, nullable=False)
    latitude = db.Column(db.String(127), unique=False, nullable=False)
    center_type_id = db.Column(
        db.Integer, db.ForeignKey("center_type.id"), nullable=False
    )
    center_state_id = db.Column(
        db.Integer, db.ForeignKey("center_state.id"), nullable=False
    )
    turns = db.relationship("Turn", backref="center", lazy=True)

    def __init__(
        self,
        name=None,
        address=None,
        phone=None,
        opens=None,
        closes=None,
        town=None,
        web=None,
        email=None,
        protocol=None,
        longitude=None,
        latitude=None,
        state=None,
        center_type=None,
    ):
        """
        Constructor para centros.

        Args:
            name (string): Un nombre.
            address (string): Una dirección.
            phone (string): Un número de teléfono.
            opens (time): Un horario de apertura.
            closes (time): Un horario de cierre.
            town (string): Un municipio.
            web (string): Página web del centro.
            email (string): Una dirección de correo.
            protocol (string): Una ruta al protocolo.
            longitude (string): Una longitud.
            latitude (string): Una latitud.
            state (CenterState): Una instancia de un estado
            center_type (CenterType): Una instancia de un tipo de centro.
        """

        self.name = name
        self.address = address
        self.phone = phone
        self.opens = opens
        self.closes = closes
        self.town = town
        self.web = web
        self.email = email
        self.protocol = protocol
        self.longitude = longitude
        self.latitude = latitude
        self.center_state = state
        self.center_type = center_type

    def serialize(self):
        """
        Devuelve un diccionario representativo del centro.

        Returns:
            dictionary: Diccionario con datos del centro.
        """
        return {
            "nombre": self.name,
            "direccion": self.address,
            "telefono": self.phone,
            "hora_apertura": self.opens.isoformat(timespec="minutes"),
            "hora_cierre": self.closes.isoformat(timespec="minutes"),
            "center_type": self.center_type.name,
            "web": self.web,
            "email": self.email,
            "id": self.id,
            "latitud": self.latitude,
            "longitud": self.longitude,
        }

    @classmethod
    def group_by_town(cls):
        """
        Agrupa en un diccionario los municipios, la cantidad de
        centros aprovados, y la cantidad de turnos de cada uno.

        Returns:
            dictionary: Diccionario con datos de los municipios.
        """

        grouped_centers = [
            list(k)
            for i, k in itertools.groupby(
                cls.order_approved_by_town(), lambda center: center.town
            )
        ]

        return list(map(cls.serialize_group, grouped_centers))

    @classmethod
    def serialize_group(cls, group):
        """
        Agrupa en un diccionario los datos de un grupo, conformado por
        el ID de un municipio, los centros aprovados en él, y la
        cantidad de turnos de cada uno.

        Returns:
            dictionary: Diccionario con datos del grupo.
        """
        return {
            "Municipio": group[0].town,
            "Centros": len(group),
            "Turnos": sum(map(lambda center: len(center.turns), group)),
        }

    @classmethod
    def order_approved_by_town(cls):
        """
        Retorna todos los centros aprovados, ordenados por ID de
        municipio.

        Returns:
            centers (list(Center)): Lista de centros ordenados por
                municipio.
        """
        return sorted(
            CenterState.get_all_aprobados(), key=lambda center: center.town
        )

    @classmethod
    def serialize_by_turns(cls):
        """
        Retorna todos los centros aprovados, ordenados por cantidad de
        turnos.

        Returns:
            centers (list(Center)): Lista de centros ordenados por
                cantidad de turnos.
        """
        return list(
            map(
                lambda center: center.__serialize_by_turns(),
                cls.order_by_turns(),
            )
        )

    def __serialize_by_turns(self):
        """
        Retorna un diccionario con el nombre del centro y la cantidad
        de turnos disponibles.

        Returns:
            dictionary: Diccionario con datos del centro.
        """
        return {
            "Nombre": self.name,
            "Turnos": len(self.turns),
        }

    @classmethod
    def order_by_turns(cls):
        """
        Retorna todos los centros aprovados, ordenados por cantidad de
        turnos.

        Returns:
            centers (list(Center)): Lista de centros ordenados por
                cantidad de turnos.
        """
        return sorted(
            CenterState.get_all_aprobados(),
            key=lambda center: len(center.turns),
            reverse=True,
        )

    def change_state(self, state_name):
        """
        Cambia el estado de un centro.

        Args:
            state_name (string):  El nombre de un estado en el que el centro
                se pued
            encontrar.
        """
        self.center_state = CenterState.find_by_name(state_name)
        db.session.commit()

    @classmethod
    def create(cls, center):
        """
        Agrega un centro a la base de datos.

        Args:
            center (Center): Una instancia de la clase Center.

        Returns:
            center: El centro creado.
        """
        return crud.create(center)

    @classmethod
    def delete(cls, center):
        """
        Borra un centro de la base de datos.

        Args:
           center (Center): Una instancia de la clase Center.
        """
        crud.delete(center)

    @classmethod
    def find_by_name(cls, a_name):
        """
        Busca un centro por nombre.

        Args:
            a_name (string): El nombre del centro a buscar.

        Returns:
            center: El primer centro encontrado con el nombre buscado.
        """
        return cls.query.filter_by(name=a_name).first()

    @classmethod
    def find_by_id(cls, asked_id):
        """
        Busca un centro que posea determinada ID.

        Args:
            asked_id (int): El ID del centro buscado.

        Returns:
            center: El primer centro que posea ese ID.
        """
        return cls.query.filter_by(id=asked_id).first()

    @classmethod
    def get_all(cls):
        """
        Busca todos los centros de la base de datos.

        Returns:
            center: Una lista de todos los centros de la base de datos.
        """
        return cls.query.all()

    def has_turn(self, date, schedule):
        """
        Retorna si existe un turno en el centro en un dia y en un bloque
        horario determinados.

        Args:
            date (date): La fecha de un dia.
            schedule (schedule): Un bloque horario.

        Returns:
            bool: True si existe el turno, False en caso contrario.
        """
        for turn in self.turns:
            if turn.has_day_and_schedule(date, schedule):
                return True
        return False

    def get_available_turns(self, date):
        """
        Retorna los bloques de horarios disponibles a partir
        de una fecha.

        Args:
            date (date): La fecha de un dia.

        Returns:
            list(Schedule): Lista de bloques de horarios
                disponibles.
        """
        turnsFromDate = filter(lambda turn: turn.has_day(date), self.turns)
        schedules = Schedule.get_unused_schedules(turnsFromDate)
        return schedules

    @classmethod
    def paginate(cls, page, limit):
        """
        Pagina todos los centros y devuelve la página pedida.

        Args:
            limit (int): Cantidad máxima de centros a devolver.
            page (int): Tanda de centros a devolver.

        Returns:
            centers: Un objeto 'Pagination' con todos los centros.
        """
        return cls.query.paginate(page, limit)

    def has_state(self, a_state):
        """
        Compara el estado recibido con el estado actual del centro.

        Args:
            a_state (string): Nombre del estado con el que comparar

        Returns:
            bool: True si el centro tiene el estado recibido, False en
                caso contrario.
        """
        return self.center_state.has_name(a_state)

    @classmethod
    def centers_with_name(cls, name):
        """
        Retorna los centros que contienen el nombre pasado por
        parámetro.

        Args:
            name (string): Un nombre de centro.

        Returns:
            list(center): Lista de centros que contienen el
                nombre.
        """
        return cls.query.filter(cls.name.contains(name))

    @classmethod
    def search_by_name_and_state(cls, state, page, limit, name=""):
        """
        Retorna los centros que contienen el nombre pasado por
        parámetro y estado, paginados por un limite.

        Args:
            state (int): Identificador de estado.
            page (int): Número de página
            limit (int): Número de límite
            name (str, optional): Un nombre. Defaults to "".

        Returns:
            list(center): Lista de centros que contienen el
                nombre y estado.
        """
        if state == "":
            return (
                cls.query.order_by(cls.name)
                .filter(cls.name.contains(name))
                .paginate(page, limit)
            )
        else:
            return (
                cls.query.order_by(cls.name)
                .filter(cls.name.contains(name), cls.center_state_id == state)
                .paginate(page, limit)
            )

    def is_pending(self):
        """
        Retorna si el estado del centro es pendiente.

        Returns:
            boolean: True si el centro es "Pendiente".
        """
        return self.center_state.name == "Pendiente"

    @classmethod
    def update_center_by_id(
        cls,
        id,
        name,
        email,
        address,
        phone,
        opens,
        closes,
        town,
        web,
        protocol,
        longitude,
        latitude,
        center_type,
    ):
        """
        Busca un centro por su id y lo actualiza en la base de datos
        con los datos recibidos.

        Args:
            id (int): La id de un centro.
            name (string): Un nombre.
            email (string): Una dirección de correo.
            address (string): Una dirección.
            phone (string): Un número de teléfono.
            opens (time): Un horario de apertura.
            closes (time): Un horario de cierre.
            town (string): Un municipio.
            web (string): Página web del centro.
            protocol (string): Una ruta al protocolo.
            longitude (string): Una longitud.
            latitude (string): Una latitud.
            center_type (CenterType): Una instancia de un tipo de
                centro.
        """
        center_aux = cls.find_by_id(id)
        center_aux.name = name
        center_aux.address = address
        center_aux.phone = phone
        center_aux.opens = opens
        center_aux.closes = closes
        center_aux.town = town
        center_aux.web = web
        center_aux.email = email
        center_aux.protocol = protocol
        center_aux.longitude = longitude
        center_aux.latitude = latitude
        center_aux.center_type_id = center_type
        db.session.commit()

    def accept(self):
        """ Cambia el estado del centro a "Aprobado" """
        self.change_state("Aprobado")

    def reject(self):
        """ Cambia el estado del centro a "Rechazado" """
        self.change_state("Rechazado")
