import re

from subprocess import Popen, PIPE
from dataclasses import dataclass

from exceptions import CantGetCoordinates


@dataclass(slots=True, frozen=True)
class Coordinates:
    longitude: float
    latitude: float


adress = "https://www.geolocation.com/ru"


def _float_coor(value: str) -> float:
    '''convert str in float, if failed raise my custom excepterror'''
    try:
        return float(value)
    except ValueError:
        raise CantGetCoordinates


def _get_coors(resp: str) -> tuple[float]:
    '''Find latitude and longitude in {adress} response,
       convert it in float and return tuple [float]'''
    latitude = re.findall(r"latitude.*\d{2}.\d{4}", resp)
    longitude = re.findall(r"longitude.*\d{2}.\d{4}", resp)
    return _float_coor(longitude[0][12:]), _float_coor(latitude[0][11:])


def _get_geoloc_response() -> str:
    '''get response from {adress}, convert it in str'''
    process = Popen(['curl', adress], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if err is not None or exit_code != 0:
        raise CantGetCoordinates
    return output.decode().strip().lower()


def get_gps_coordinates() -> Coordinates:
    resp = _get_geoloc_response()
    coors = _get_coors(resp)
    return Coordinates(longitude=coors[0],
                       latitude=coors[1])


if __name__ == "__main__":
    print(get_gps_coordinates())
