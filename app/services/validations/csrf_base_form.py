from wtforms import Form
from wtforms.csrf.session import SessionCSRF
from flask import session


class CsrfBaseForm(Form):
    """
    Clase que activa las configuraciones para la proteccion contra CSRF
    """

    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = b"EPj00jpfj8Gx1SjnyLxwBBSQfnQ9DJYe0Ym"

        @property
        def csrf_context(self):
            return session
