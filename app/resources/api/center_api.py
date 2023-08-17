from json import dumps
from flask import Response
from flask_restful import Resource
from app.models.center import Center


class CenterApi(Resource):
    "Clase para realizar la API de obtención de un centro específico."

    def get(self, center_id):
        """
        Retorna un centro específico dado un id.
        - Si el id no pertenece a un centro existente, retorna 404
        - Si el id pertenece a un centro que no está aprobado para
            publicación, retorna 403
        - Si el id es válido, retorna la información del centro en JSON
            y el código de operación 200.
        - Si el id es válido, retorna la información del centro en JSON
            y el código de operación 200.

        Args:
            center_id (int): El id del centro a buscar.

        Returns:
            response: Instancia de la clase Response con la información
                de un centro aprobado, en formato JSON, con un código
                HTTP.
        """
        try:
            center = Center.find_by_id(center_id)
            if not center:
                return Response(
                    '{"error":"Centro no encontrado"}',
                    status=404,
                    mimetype="application/json",
                )

            if not center.has_state("Aprobado"):
                return Response(
                    '{"error":"El centro no está aprobado para publicación"}',
                    status=403,
                    mimetype="application/json",
                )

            return Response(
                dumps(center.serialize()),
                status=200,
                mimetype="application/json",
            )
        except:
            return Response(
                '{"error": "Algo falló en el servidor"}',
                status=500,
                mimetype="application/json",
            )
