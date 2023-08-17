from app.models.user import User
from flask import session, abort


def is_pending(center):
    """
    Retorna si un centro está en estado pendiente.

    Args:
        center (Center): Un centro

    Returns:
        boolean: True si el centro está en estado pendiente
    """
    return center.is_pending()
