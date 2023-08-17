from app.models.user import User
from flask import session, abort


def check(user_email, permission):
    """
    Busca un permiso dentro de los roles de un usuario.

    Args:
        user_email (string): El email del usuario a consultar.
        permission (string): El nombre del permiso a buscar.
    Details:
        Le pide al objeto User que informe si el usuario tiene
        el permiso pasado como paramtro
    Returns:
        bool: Retorna verdadero si en sus roles se encuentra el
            permiso buscado.
    """
    return User.has_permission(user_email, permission)


def is_active(user_email):
    """
    Verifica que el usuario no esté bloqueado. De ser así
    se cierra su sesión y se lo envía a una página de error.

    Args:
        user_email (string): El email del usuario a consultar.
    """
    user = User.find_by_email(user_email)
    if not user.is_active():
        del session["user"]
        session.clear()
        abort(401)
