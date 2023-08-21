from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Coordinates:
    longitude: float
    latitude: float


def get_gps_coordinates() -> Coordinates:
    return Coordinates(longitude=10, latitude=20)
