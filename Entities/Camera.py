import uuid
from enum import Enum

from Entities.User import User


class CameraType(Enum):
    UNDEFINED = 0
    DIGITAL_CMOS = 1
    DIGITAL_CCD = 2
    FULL_FRAME_35_MM = 3
    HALF_FRAME_35_MM = 4
    FRAME_6x6_120 = 5
    FRAME_6x7_120 = 6
    FRAME_3x4_5_120 = 7
    SHEET = 8


class Camera():
    def __init__(self,
                 brand: str,
                 model: str,
                 camera_type: CameraType,
                 owner: User | None = None,
                 uid: str | uuid.UUID | None = None):
        if uid is None:
            self.uid = uuid.uuid4().__str__()
        else:
            self.uid = uid.__str__() if type(uid) is uuid.UUID else uuid.UUID(uid).__str__()

        self.brand = brand
        self.model = model
        self.camera_type = camera_type
        self.owner = owner

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "brand": self.brand,
            "model": self.model,
            "camera_type": self.camera_type.value,
            "camera_type_name": self.camera_type,
            "owner": self.owner.uid
        }
