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
class TempHumidity(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TEMPERATURE_FIELD_NUMBER: builtins.int
    HUMIDITY_FIELD_NUMBER: builtins.int
    temperature: builtins.float
    humidity: builtins.float
    def __init__(
        self,
        *,
        temperature: builtins.float = ...,
        humidity: builtins.float = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["humidity", b"humidity", "temperature", b"temperature"]) -> None: ...

global___TempHumidity = TempHumidity

@typing_extensions.final
class MeteoData(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SENSOR_ID_FIELD_NUMBER: builtins.int
    METEO_DATA_FIELD_NUMBER: builtins.int
    TIMESTAMP_FIELD_NUMBER: builtins.int
    sensor_id: builtins.int
    @property
    def meteo_data(self) -> global___TempHumidity: ...
    timestamp: builtins.int
    def __init__(
        self,
        *,
        sensor_id: builtins.int = ...,
        meteo_data: global___TempHumidity | None = ...,
        timestamp: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["meteo_data", b"meteo_data"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["meteo_data", b"meteo_data", "sensor_id", b"sensor_id", "timestamp", b"timestamp"]) -> None: ...

global___MeteoData = MeteoData

@typing_extensions.final
class PollutionData(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CO2_FIELD_NUMBER: builtins.int
    SENSOR_ID_FIELD_NUMBER: builtins.int
    TIMESTAMP_FIELD_NUMBER: builtins.int
    co2: builtins.float
    sensor_id: builtins.int
    timestamp: builtins.int
    def __init__(
        self,
        *,
        co2: builtins.float = ...,
        sensor_id: builtins.int = ...,
        timestamp: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["co2", b"co2", "sensor_id", b"sensor_id", "timestamp", b"timestamp"]) -> None: ...

global___PollutionData = PollutionData