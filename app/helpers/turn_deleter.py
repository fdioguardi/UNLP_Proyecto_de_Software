from app.models.turn import Turn


def delete_turns(center):
    """
    Elimina todos los turnos de un centro

    Args:
<<<<<<< HEAD
        center (Center): El centro al que se le 
        borraran sus turnos.
=======
>>>>>>> master
        center (Center): El centro al que se le
            borraran sus turnos.
    """
    for turn in center.turns:
        Turn.delete(turn)
