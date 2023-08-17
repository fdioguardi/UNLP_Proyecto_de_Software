import re
import js_regex


def validate_telephone(telephone):
    """
    Retorna si un télefono es sintácticamente válido.

    Args:
        telephone (string): Un teléfono.

    Returns:
        bool: True si el teléfono es válido.
    """
    regex = js_regex.compile("^(\d{3})[-]?(\d{3})[-]?(\d{4})$")
    return regex.search(telephone)


def validate_email(email):
    """
    Retorna si un email es sintácticamente válido.

    Args:
        email (string): Un email.

    Returns:
        bool: True si el email es válido.
    """
    regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
        # quoted-string
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'
        r")@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$",
        re.IGNORECASE,
    )
    return regex.search(email)


def validate_url(url):
    """
    Retorna si un url es sintácticamente válido.

    Args:
        url (string): Un url.

    Returns:
        bool: True si el url es válido.
    """
    regex = js_regex.compile(
        "(([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:"
        "www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??"
        "(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?"
    )
    return regex.search(url)


def validate_time(time):
    """
    Retorna si un tiempo es sintácticamente válido.

    Args:
        time (string): Un tiempo.

    Returns:
        bool: True si el tiempo es válido.
    """
    return re.match("^([01]?[0-9]|2[0-3]):[0-5][0-9]$", time)
