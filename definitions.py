"""
Contains all static definitions
"""

mime_file_extension: dict[str, str] = {
    "image/jpeg": "jpeg",
    "image/png": "png",
    "image/heic": "heic",
    "image/tiff": "tiff",
    "image/x-nikon-nef": "nef",
    "image/x-adobe-dng": "dng",
    "image/x-canon-cr3": "cr3",
    "image/x-canon-cr2": "cr2",
    "image/x-canon-crw": "crw"
}

postprocess_file_types: dict[str, str] = {
    "image/x-nikon-nef": "nef",
    "image/x-adobe-dng": "dng",
    "image/x-canon-cr3": "cr3",
    "image/x-canon-cr2": "cr2",
    "image/x-canon-crw": "crw"
}

