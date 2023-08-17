from flask_restful import Resource
from flask import request, Response
from app.models.center import Center
import datetime
import json


class TurnListAPI(Resource):
    "Clase para realizar la API de listado de turnos."

    def get(self, id):
        """
        Retorna un listado de turnos disponibles en una fecha
        para un centro determinado por id.
        - Si no se brinda una fecha, se utiliza el día
            de hoy
        - Si el centro_id no pertenece a un centro existente
            retorna 500.
        - Si los datos son validos, retorna un listado de
            turnos disponibles en JSON y el codigo de
            operacion 200.

        Args:
            id (int): La id del centro pasada por URL.

        Returns:
            obj: Listado de turnos disponibles en JSON.
            codop: Codigo de operacion.
        """
        try:
            if "fecha" in request.args:
                fecha = datetime.datetime.strptime(
                    request.args["fecha"], "%Y-%m-%d"
                ).date()
            else:
                fecha = datetime.date.today()

            center = Center.find_by_id(id)
            if not center:
                return Response(
                    '{"error": "El centro no ha sido encontrado"}',
                    status=404,
                    mimetype="application/json",
                )

            available_turns = center.get_available_turns(fecha)
            turnos = []
            for turn in available_turns:
                turnos.append(
                    {
                        "centro_id": id,
                        "hora_inicio": turn.start.strftime("%H:%M"),
                        "hora_fin": turn.end.strftime("%H:%M"),
                        "fecha": fecha.strftime("%Y-%m-%d"),
                        "turno_id": turn.id,
                    }
                )
            return Response(
                json.dumps({"turnos": turnos}),
                status=200,
                mimetype="application/json",
            )

        except:
            return Response(
                '{"error": "Algo falló en el servidor"}',
                status=500,
                mimetype="application/json",
            )
