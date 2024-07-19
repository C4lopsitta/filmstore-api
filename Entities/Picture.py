
class Picture:
    def __init__(self,
                 thumbnail: str,
                 db_id: int = None,
                 posted: bool = False,
                 printed: bool = False,
                 description: str = None,
                 location: str = None,
                 aperture: str = None,
                 shutter_speed: str = None):
        self.db_id = db_id
        self.thumbnail = thumbnail
        self.posted = posted
        self.description = description
        self.printed = printed
        self.location = location
        self.aperture = aperture
        self.shutter_speed = shutter_speed
