from app.models.user import User


def has_role(user, role_name):
    """
    Retorna si el usuario tiene el rol determinado.

    Args:
        user (User): El usuario a consultar.
        role_name (string): El nombre del rol a buscar.
    Details:
        Le pide al objeto User que informe si el usuario tiene
        el rol pasado como paramtro
    Returns:
        bool: Retorna verdadero si en sus roles se encuentra el
            rol buscado.
    """
    return user.user_has_role(role_name)


def email_has_role(email_user, role_name):
    return User.has_role(email_user, role_name)
