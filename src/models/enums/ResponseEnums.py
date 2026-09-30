from enum import Enum


class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"
    FILE_SIZE_EXCEEDS_LIMIT = "File size exceeds the maximum allowed size"
    FILE_INVALID = "File is invalid"
    FILE_VALID = "File is valid"
    FILE_UPLOAD_SUCCESS = "File uploaded successfully"
    FILE_UPLOAD_FAILED = "File upload failed"
    FILE_NAME_INVALID = "File name is invalid"
