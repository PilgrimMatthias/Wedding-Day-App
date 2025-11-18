from dataclasses import dataclass


@dataclass
class Photo:
    """
    Photo instance for database
    """

    image_name: str = None
    image_caption: str = None
    image_path: str = None
