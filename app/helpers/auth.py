def authenticated(session):
    """
    Devuelve el email del usario logeado en la sesión actual.

    Args:
        session (Session): Diccionario que contiene informacion de la sesion
            actual de los  usurios logeados.

    Returns:
            string: Un string que indica el email del usuario.
    """
    return session.get("user")
