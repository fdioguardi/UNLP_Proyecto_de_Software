from json import dumps
from flask import Response
from flask_restful import Resource
from app.models.center_type import CenterType


class CenterTypeApi(Resource):
    "Clase para realizar la API de obtención de tipos de centro."

    def get(self):
        """
        Retorna un listado con los tipos de centro existentes.
        - Si ocurre un error inesperado en el servidor, retorna 500.
        - Si no se produce ningún error, retorna los tipos de centro en
            JSON y el código de operación 200.

        Returns:
            response: Instancia de la clase Response con un listado de
                tipos de centro en formato JSON y el código HTTP.
        """
        try:
            types = CenterType.serialized_center_types()
            return Response(
                dumps(
                    {
                        "tipos_de_centro": types,
                        "total": len(types),
                    }
                ),
                status=200,
                mimetype="application/json",
            )

        except:
            return Response(
                '{"error": "Algo falló en el servidor"}',
                status=500,
                mimetype="application/json",
            )
