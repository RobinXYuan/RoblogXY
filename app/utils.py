from enum import Enum


class MessageTypes(Enum):
    success = 'success'
    error = 'error'
    normal = 'normal'