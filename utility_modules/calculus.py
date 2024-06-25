import math


def calculate_vector_magnitude(vector_coords):
    magnitude_vector = math.sqrt(vector_coords[0]**2 + vector_coords[1]**2)
    return magnitude_vector

def calculate_angle_north(vector_desired, vector_north):
    signed_angle = math.atan2(vector_desired[1], vector_desired[0]) - math.atan2(vector_north[1], vector_north[0])
    angle_degrees = math.degrees(signed_angle) % 360
    return angle_degrees
