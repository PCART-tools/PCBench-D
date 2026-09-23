@_api.deprecated("3.8")
def rotation_about_vector(v, angle):
    """
    Produce a rotation matrix for an angle in radians about a vector.
    """
    return _rotation_about_vector(v, angle)
