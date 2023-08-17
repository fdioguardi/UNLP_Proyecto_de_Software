from app.models.configuration import Configuration


def is_enabled():
    """
    Informa si la pagina esta habilitada.

    Details:
        Le pide al objeto Configuracion que informe si la pagina esta
        habilitada.
    Returns:
            bool: Un booleano que indica si la pagina esta habilitada
    """
    return Configuration.is_enabled()
