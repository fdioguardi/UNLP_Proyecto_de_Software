from app.db import db


def create(model):
    """
    Guarda y actualiza el model en la base de datos

    Args:
       model (Modelo): Instancia de una clase que esta en la
        base de datos.

    Returns:
        model: Objeto que se guarda en la base de datos
    """
    db.session.add(model)
    db.session.commit()
    return model


def delete(model):
    """
    Borra y actualiza el model en la base de datos

    Args:
        model (Modelo): Instancia de una clase que esta en la
            base de datos.
    """
    db.session.delete(model)
    db.session.commit()
