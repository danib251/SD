"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class ProcessedMeteoData(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LB_ID_FIELD_NUMBER: builtins.int
    AIR_WELLNESS_FIELD_NUMBER: builtins.int
    TIMESTAMP_FIELD_NUMBER: builtins.int
    lb_id: builtins.int
    air_wellness: builtins.float
    timestamp: builtins.int
    def __init__(
        self,
        *,
        lb_id: builtins.int = ...,
        air_wellness: builtins.float = ...,
        timestamp: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["air_wellness", b"air_wellness", "lb_id", b"lb_id", "timestamp", b"timestamp"]) -> None: ...

global___ProcessedMeteoData = ProcessedMeteoData

@typing_extensions.final
class ProcessedPollutionData(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    POLLUTION_COEFFICIENT_FIELD_NUMBER: builtins.int
    LB_ID_FIELD_NUMBER: builtins.int
    TIMESTAMP_FIELD_NUMBER: builtins.int
    pollution_coefficient: builtins.float
    lb_id: builtins.int
    timestamp: builtins.int
    def __init__(
        self,
        *,
        pollution_coefficient: builtins.float = ...,
        lb_id: builtins.int = ...,
        timestamp: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["lb_id", b"lb_id", "pollution_coefficient", b"pollution_coefficient", "timestamp", b"timestamp"]) -> None: ...

global___ProcessedPollutionData = ProcessedPollutionData