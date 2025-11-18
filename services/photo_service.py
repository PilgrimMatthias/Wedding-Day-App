import os, io, zipfile
from supabase import create_client, Client
from dotenv import load_dotenv
from models.photo import Photo

# Load environment variables from .env
load_dotenv()


class PhotoService:
    """Photo Service

    Service that manages all connections between user and database.
    """

    def __init__(self):
        # Setting connection to db
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SERVICE_KEY")
        self.supabase: Client = create_client(url, key)

        # Schemas and tables
        self.db_schema = os.environ.get("DATABASE_SCHEMA")
        self.db_table = os.environ.get("DATABASE_TABLE")
        self.db_storage = os.environ.get("DATABASE_STORAGE")

    def upload_photo(self, file_name: str, caption: str, file_path: str) -> None:
        """
        Uploading photo to database table and storage

        Args:
            file (_type_): file (image) name
            name (_type_): file (image) name
            caption (_type_): description added to the image
            path (_type_): path to local file
        """

        # Open file from temp folder and upload to storage
        self._upload_image(file_name=file_name, file_path=file_path)

        # Get public url to the file
        public_url = self._get_public_url(file_name)

        # Create instance (row) to db table
        photo = Photo(
            image_name=file_name,
            image_caption=caption,
            image_path=public_url,
        )

        # Upload row to table db
        self._add_db_instance(photo.__dict__)

    def get_all_photos(self):
        """
        Get all photos information in database

        Returns:
            list<dict> : list with all the photos
        """
        response = (
            self.supabase.schema(self.db_schema)
            .table(self.db_table)
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        return [
            Photo(
                image_name=p.get("image_name"),
                image_caption=p.get("image_caption"),
                image_path=p.get("image_path"),
            )
            for p in response.data
        ]

    def download_photos(self):
        """
        Downloading all photos and adding them to zip buffer for download

        Returns:
            zip buffer: packed photos for download
        """
        photos = self.supabase.storage.from_(self.db_storage).list()

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for photo in photos:
                if not photo["name"].lower().endswith((".jpg", ".jpeg", ".png")):
                    continue
                data = self.supabase.storage.from_(self.db_storage).download(
                    photo["name"]
                )
                if data:
                    zipf.writestr(photo["name"], data)

        zip_buffer.seek(0)

        return zip_buffer

    def _add_db_instance(self, photo: dict) -> None:
        """
        Add instance to database

        Args:
            photo (dict): row to the database
        """
        self.supabase.schema(self.db_schema).table(self.db_table).insert(
            photo
        ).execute()

    def _upload_image(self, file_name: str, file_path: str) -> None:
        """
        Uploading image to database storage

        Args:
            file (str): file name
            path (str): path to the file
        """
        with open(
            file_path,
            "rb",
        ) as file:
            self.supabase.storage.from_(self.db_storage).upload(
                file=file,
                path=file_name,
                file_options={"content-type": "image/*"},
            )

    def _get_public_url(self, file_name: str) -> str:
        """
        Get public url to file added to the storage

        Args:
            file_name (_type_): name of the image in the storage

        Returns:
            string: public url to photo
        """
        return self.supabase.storage.from_(self.db_storage).get_public_url(file_name)
