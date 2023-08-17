from flask_restful import Resource, reqparse
from flask import Response
from app.models.turn import Turn
from app.models.schedule import Schedule
from app.models.center import Center
from app.helpers import regex
import datetime
import json


class TurnReservationAPI(Resource):
    "Clase para realizar la API de reserva de turnos."

    def __init__(self):
        """
        Inicializa la API de turnos con un RequestParser
        asignando diferentes argumentos que debe tener
        un pedido con un json hecho a la misma.
        """
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "centro_id", type=int, required=True, location="json"
        )
        self.reqparse.add_argument(
            "email_donante", type=str, required=True, location="json"
        )
        self.reqparse.add_argument(
            "telefono_donante", type=str, location="json"
        )
        self.reqparse.add_argument(
            "hora_inicio", required=True, location="json"
        )
        self.reqparse.add_argument("hora_fin", required=True, location="json")
        self.reqparse.add_argument("fecha", required=True, location="json")
        super(TurnReservationAPI, self).__init__()

    def post(self, id):
        """
        Recibe un json con un objeto y parsea sus datos
        para agregar un turno en la base de datos.
        - Si ocurre algun error con la base de datos,
            retorna 500
        - Si el centro_id no es igual a la id de la URL,
            retorna 400
        - Si el telefono no es sintacticamente valido,
            retorna 400
        - Si el email no es sintacticamente valido,
            retorna 400
        - Si los horarios no son sintacticamente valido,
            retorna 400
        - Si la hora_inicio y/o la hora_fin no pertenecen
            a un bloque horario existente, retorna 404.
        - Si el centro_id no pertenece a un centro existente
            retorna 404.
        - Si el dia no es sintacticamente valido,
            retorna 400
        - Si el dia es menor que hoy,
            retorna 400
        - Si el centro ya posee un turno en la fecha y bloque
            horario indicados, retorna 403.
        - Si se puede crear el turno y es válido, retorna
            el turno en JSON y el codigo de operacion 201.

        Args:
            id (int): La id del centro pasada por URL.

        Returns:
            obj: Si es exitoso retorna un objeto en json.
            codop: Codigo de operacion.
        """
        args = self.reqparse.parse_args(strict=True)

        try:
            if id != args["centro_id"]:
                return Response(
                    '{"error": "Las id pasadas no concuerdan"}',
                    status=400,
                    mimetype="application/json",
                )

            if not regex.validate_telephone(args["telefono_donante"]):
                return Response(
                    '{"error": "El formato del telefono no es válido"}',
                    status=400,
                    mimetype="application/json",
                )

            if not regex.validate_email(args["email_donante"]):
                return Response(
                    '{"error": "El formato del email no es válido"}',
                    status=400,
                    mimetype="application/json",
                )

            try:
                hora_inicio = datetime.datetime.strptime(
                    args["hora_inicio"], "%H:%M"
                ).time()
                hora_fin = datetime.datetime.strptime(
                    args["hora_fin"], "%H:%M"
                ).time()
            except:
                return Response(
                    '{"error": "El formato de las horas no es válido"}',
                    status=400,
                    mimetype="application/json",
                )

            schedule = Schedule.find_by_times(hora_inicio, hora_fin)
            if not schedule:
                return Response(
                    '{"error": "El bloque horario no ha sido encontrado"}',
                    status=404,
                    mimetype="application/json",
                )

            center = Center.find_by_id(args["centro_id"])
            if not center:
                return Response(
                    '{"error": "El centro no ha sido encontrado"}',
                    status=404,
                    mimetype="application/json",
                )

            try:
                fecha = datetime.datetime.strptime(
                    args["fecha"], "%Y-%m-%d"
                ).date()
            except:
                return Response(
                    '{"error": "El formato de la fecha no es válido"}',
                    status=400,
                    mimetype="application/json",
                )

            if fecha < datetime.date.today():
                return Response(
                    '{"error": "La fecha ingresada es menor a hoy"}',
                    status=400,
                    mimetype="application/json",
                )

            if center.has_turn(fecha, schedule):
                return Response(
                    '{"error": "El turno pedido ya está ocupado"}',
                    status=403,
                    mimetype="application/json",
                )

            Turn.create(
                Turn(
                    email=args["email_donante"],
                    day=fecha,
                    center=center,
                    schedule=schedule,
                )
            )
            return Response(
                json.dumps({"atributos": args}),
                status=201,
                mimetype="application/json",
            )

        except:
            return Response(
                '{"error": "Algo falló en el servidor"}',
                status=500,
                mimetype="application/json",
            )
