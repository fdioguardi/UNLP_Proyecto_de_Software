from json import dumps
from flask import Response
from flask_restful import Resource
from app.models.center import Center


class TownApi(Resource):
    """
    Clase para realizar la API de centros y turnos ordenados por
    municipios.
    """

    def get(self):
        """
        Retorna un listado con municipios, la cantidad de centros, y la
            cantidad de turnos total en todos esos centros.
        - Si ocurre un error inesperado en el servidor, retorna 500.
        - Si no se produce ningún error, retorna los datos en formato
            JSON y el código de operación 200.

        Returns:
            response: Instancia de la clase Response con un listado de
                municipios, cantidad de centros, y cantidad de turnos,
                en formato JSON y el código HTTP.
        """
        try:
            return Response(
                dumps({"Municipios": Center.group_by_town()}),
                status=200,
                mimetype="application/json",
            )

        except:
            return Response(
                '{"error": "Algo falló en el servidor"}',
                status=500,
                mimetype="application/json",
            )
