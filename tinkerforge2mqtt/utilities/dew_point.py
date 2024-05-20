import math


SV_PRESSURE = 6.112  # saturation vapor pressure at 0°C


def calculate_dew_point(
    temperature: int | float,  # Temperature in degrees Celsius
    humidity: int | float,  # Relative Humidity in %
) -> float:  # Returns: Dew point temperature in degrees Celsius
    """
    Calculate the dew point temperature given the temperature and relative humidity
    using the Magnus formula.

    Examples:
    >>> round(calculate_dew_point(temperature=18, humidity=40), 1)
    4.2
    >>> round(calculate_dew_point(temperature=22, humidity=70), 1)
    16.3
    >>> round(calculate_dew_point(temperature=30, humidity=50), 1)
    18.4
    >>> round(calculate_dew_point(temperature=-5, humidity=80), 1)
    -7.6
    """
    # Constants for the Magnus formula
    if temperature > 0:
        # above freezing
        a = 17.62  # °C
        b = 243.12  # °C
    else:
        # below freezing
        a = 22.46  # °C
        b = 272.62  # °C

    es = SV_PRESSURE * math.exp((a * temperature) / (b + temperature))  # saturation vapor pressure
    e = es * (humidity / 100.0)  # actual vapor pressure

    # Solve for the dew point temperature:
    dew_point_temperature = (b * math.log(e / SV_PRESSURE)) / (a - math.log(e / SV_PRESSURE))

    return dew_point_temperature
