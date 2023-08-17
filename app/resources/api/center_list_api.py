import re
from datetime import datetime
from json import dumps, loads
from flask import request, Response
from flask_restful import Resource, reqparse
from app.models.center import Center
from app.models.configuration import Configuration
from app.models.center_type import CenterType
from app.models.center_state import CenterState
from app.helpers import regex
import requests

class CenterListApi(Resource):
    "Clase para realizar la API de vista y creación de centros."


    def get(self):
        """
        Retorna un listado de centros aprobados.

        Returns:
            response: Instancia de la clase Response con un listado de
                centros aprobados en JSON y el código HTTP.
        """
        try:
            page = int(request.args.get("page", 1))
            all = request.args.get("all", False)
            if all == "True":
                centers = CenterState.get_all_aprobados()
            else:
                centers = CenterState.find_by_name(
                    "Aprobado"
                ).paginated_centers(page, Configuration.items_per_page())
            serialized_centers = [center.serialize() for center in centers]
            return Response(
                dumps(
                    {
                        "centros": serialized_centers,
                        "total": len(serialized_centers),
                        "pagina": page,
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

    def es_robot(self,token):
        """ Validating recaptcha response from google server
        Returns True captcha test passed for submitted form else returns False.
        """
        secret = "" # removed for secrecy
        payload = {'response':token, 'secret':secret}
        response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
        response_text = loads(response.text)
        return not response_text['success']

    def post(self):
        """
        Recibe un JSON con un objeto y parsea sus datos
        para agregar un centro a la base de datos.
        - Si con el token se detecta que no es humano, retorna 400.
        - Si el telefono no es sintácticamente válido, retorna 400.
        - Si el url no es sintacticamente válido, retorna 400.
        - Si el email no es sintacticamente válido, retorna 400.
        - Si los horarios no son sintácticamente válidos, retorna 400.
        - Si el tipo de centro no es válido, retorna 403.
        - Si ocurre un error inesperado en el servidor, retorna 500.
        - Si comprueba que no es un boot y se puede crear el turno y es válido, retorna el turno en
            JSON y el código de operación 201.

        Returns:
            response: Instancia de la clase Response con un listado de
                centros aprobados en JSON y el código HTTP.
        """
        parser = self.initialize_parser()
        args = parser.parse_args(strict=True)
        try:
            if self.es_robot(args["token"]):
                return Response(
                    '{"error":"No se permiten boots en esta página"}',
                    status=400,
                    mimetype="application/json",
                )

            if not regex.validate_telephone(args["telefono"]):
                return Response(
                    '{"error":"El número de telefono ingresado es inválido"}',
                    status=400,
                    mimetype="application/json",
                )

            if regex.validate_time(args["hora_apertura"]):
                hora_apertura = datetime.strptime(
                    args["hora_apertura"], "%H:%M"
                ).time()

            else:
                return Response(
                    '{"error":"El horario de apertura ingresado es inválido"}',
                    status=400,
                    mimetype="application/json",
                )

            if regex.validate_time(args["hora_cierre"]):
                hora_cierre = datetime.strptime(
                    args["hora_cierre"], "%H:%M"
                ).time()
            else:
                return Response(
                    '{"error":"El horario de cierre ingresado es inválido"}',
                    status=400,
                    mimetype="application/json",
                )

            if args["web"]:
                web = args["web"]

                if not regex.validate_url(web):
                    return Response(
                        '{"error":"El url ingresado no es válido"}',
                        status=400,
                        mimetype="application/json",
                    )
            else:
                web = ""

            if args["email"]:
                email = args["email"]

                if not regex.validate_email(email):
                    return Response(
                        '{"error":"El email ingresado no es válido"}',
                        status=400,
                        mimetype="application/json",
                    )
            else:
                email = ""

            center_type = CenterType.find_by_name(args["tipo"])
            if not center_type:
                return Response(
                    '{"error":"No se encontró el tipo de centro solicitado"}',
                    status=404,
                    mimetype="application/json",
                )

            Center.create(
                Center(
                    name=args["nombre"],
                    address=args["direccion"],
                    phone=args["telefono"],
                    opens=hora_apertura,
                    closes=hora_cierre,
                    center_type=center_type,
                    town=args["municipio_id"],
                    latitude=str(args["latitud"]),
                    longitude=str(args["longitud"]),
                    web=web,
                    email=email,
                    state=CenterState.find_by_name("Pendiente"),
                )
            )

            return Response(
                dumps(
                    {
                        "nombre": args["nombre"],
                        "direccion": args["direccion"],
                        "telefono": args["telefono"],
                        "hora_apertura": args["hora_apertura"],
                        "hora_cierre": args["hora_cierre"],
                        "tipo": center_type.name,
                        "municipio_id": args["municipio_id"],
                        "latitud": args["latitud"],
                        "longitud": args["longitud"],
                        "web": web,
                        "email": email,
                    }
                ),
                status=201,
                mimetype="application/json",
            )

        except:
            return Response(
                '{"error": "Algo falló en el servidor"}',
                status=500,
                mimetype="application/json",
            )

    def initialize_parser(self):
        """
        Inicializa el parser que recibirá los parámetros del JSON.

        Returns:
            parser: Instancia de la clase RequestParser, con los
                parámetros cargados.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("nombre", type=str, required=True)
        parser.add_argument("direccion", type=str, required=True)
        parser.add_argument("telefono", type=str, required=True)
        parser.add_argument("hora_apertura", type=str, required=True)
        parser.add_argument("hora_cierre", type=str, required=True)
        parser.add_argument("tipo", type=str, required=True)
        parser.add_argument("municipio_id", type=int, required=True)
        parser.add_argument("latitud", type=float, required=True)
        parser.add_argument("longitud", type=float, required=True)
        parser.add_argument("web", type=str)
        parser.add_argument("email", type=str)
        parser.add_argument("token", type=str, required=True)

        return parser
