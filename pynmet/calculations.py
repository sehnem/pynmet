from numpy import sin, cos, arctan2, radians, degrees


def avg_wind(wind_direction):
    x = cos(radians(wind_direction))
    y = sin(radians(wind_direction))
    direction_avg = (degrees(arctan2(x, y)))
    return (360 + direction_avg) % 360
