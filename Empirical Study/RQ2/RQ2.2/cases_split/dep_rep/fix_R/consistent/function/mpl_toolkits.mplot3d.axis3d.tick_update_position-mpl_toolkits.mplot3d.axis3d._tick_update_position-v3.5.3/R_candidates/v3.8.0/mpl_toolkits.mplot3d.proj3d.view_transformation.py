@_api.deprecated("3.8")
def view_transformation(E, R, V, roll):
    """
    Return the view transformation matrix.

    Parameters
    ----------
    E : 3-element numpy array
        The coordinates of the eye/camera.
    R : 3-element numpy array
        The coordinates of the center of the view box.
    V : 3-element numpy array
        Unit vector in the direction of the vertical axis.
    roll : float
        The roll angle in radians.
    """
    u, v, w = _view_axes(E, R, V, roll)
    M = _view_transformation_uvw(u, v, w, E)
    return M
