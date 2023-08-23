import re

from subprocess import Popen, PIPE
from dataclasses import dataclass

from exceptions import CantGetCoordinates


@dataclass(slots=True, frozen=True)
class Coordinates:
    longitude: float
    latitude: float


adress = "https://www.geolocation.com/ru"


def float_coor(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise CantGetCoordinates


def get_coors(resp):
    latitude = re.findall(r"latitude.*\d{2}.\d{4}", resp)
    longitude = re.findall(r"longitude.*\d{2}.\d{4}", resp)
    return float_coor(longitude[0][12:]), float_coor(latitude[0][11:])


def get_gps_coordinates() -> Coordinates:
    process = Popen(['curl', adress], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if err is not None or exit_code != 0:
        raise CantGetCoordinates
    coors = get_coors(output.decode().strip().lower())
    return Coordinates(longitude=coors[0],
                       latitude=coors[1])


if __name__ == "__main__":
    print(get_gps_coordinates())
