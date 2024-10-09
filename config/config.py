import json
from typing import TextIO


class Config:
    def __init__(self, file: TextIO):
        config_json = json.loads(file.read())
        file.close()

        images_config = config_json['images']
        data_config = config_json['data']
        authentication_config = config_json['authentication']

        self.thumbnail_folder = images_config['thumbnail_folder']
        self.temporary_files_folder = images_config['temporary_files_folder']
        self.original_folder = images_config['original_folder']
        self.allow_raw_upload = images_config['allow_raw_upload']
        self.allow_raw_post_processing = images_config['allow_raw_post_processing']
        self.disable_thumbnail_compression = images_config['disable_thumbnail_compression']
        self.include_exif_in_image_metadata = images_config['include_exif_in_image_metadata']

        self.database_file_name = data_config['database_file_name']

        self.use_user_auth = authentication_config['use_user_auth']
        self.allow_user_creation = authentication_config['allow_user_creation']
