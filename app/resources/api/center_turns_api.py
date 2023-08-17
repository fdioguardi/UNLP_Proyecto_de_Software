from json import dumps
from flask import Response, request
from flask_restful import Resource
from app.models.center import Center


class CenterTurnsApi(Resource):
    """
    Clase para realizar la API de centros ordenados por cantidad de
    turnos.
    """

    def get(self):
        """
        Retorna un listado con el top de centros, según la cantidad de
            turnos historica que se hayan sacado.
        - Si ocurre un error inesperado en el servidor, retorna 500.
        - Si no se produce ningún error, retorna los datos en formato
            JSON y el código de operación 200.

        Args:

        Returns:
            response: Instancia de la clase Response con un listado de
                municipios, cantidad de centros, y cantidad de turnos,
                en formato JSON y el código HTTP.
        """
        amount = int(request.args.get("amount", 5))

        # try:
        return Response(
            dumps({"Centros": Center.serialize_by_turns()[:amount]}),
            status=200,
            mimetype="application/json",
        )

        # except:
        #     return Response(
        #         '{"error": "Algo falló en el servidor"}',
        #         status=500,
        #         mimetype="application/json",
        #     )
