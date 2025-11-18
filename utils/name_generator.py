import uuid
from datetime import datetime


def generate_file_name(extension) -> str:
    """
    Generate safe unique file name

    Args:
        extension (str): file extenstion

    Returns:
        str: new file name
    """

    return "{0}.{1}.{2}".format(
        str(uuid.uuid4().hex), datetime.now().timestamp(), extension
    )
