from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Client(_message.Message):
    __slots__ = ["CID", "data"]
    CID: str
    CID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: str
    def __init__(self, CID: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...

class ID(_message.Message):
    __slots__ = ["ID"]
    ID: str
    ID_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, ID: _Optional[str] = ...) -> None: ...

class Order(_message.Message):
    __slots__ = ["CID", "OID", "data"]
    CID: str
    CID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    OID: str
    OID_FIELD_NUMBER: _ClassVar[int]
    data: str
    def __init__(self, OID: _Optional[str] = ..., CID: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...

class Product(_message.Message):
    __slots__ = ["PID", "data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    PID: str
    PID_FIELD_NUMBER: _ClassVar[int]
    data: str
    def __init__(self, PID: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...

class Reply(_message.Message):
    __slots__ = ["description", "error"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    description: str
    error: int
    def __init__(self, error: _Optional[int] = ..., description: _Optional[str] = ...) -> None: ...
