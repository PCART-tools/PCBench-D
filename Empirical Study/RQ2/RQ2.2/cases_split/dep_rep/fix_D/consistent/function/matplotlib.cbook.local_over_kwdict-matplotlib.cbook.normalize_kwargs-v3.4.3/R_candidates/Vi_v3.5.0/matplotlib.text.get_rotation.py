def get_rotation(rotation):
    """
    Return *rotation* normalized to an angle between 0 and 360 degrees.

    Parameters
    ----------
    rotation : float or {None, 'horizontal', 'vertical'}
        Rotation angle in degrees. *None* and 'horizontal' equal 0,
        'vertical' equals 90.

    Returns
    -------
    float
    """
    try:
        return float(rotation) % 360
    except (ValueError, TypeError) as err:
        if cbook._str_equal(rotation, 'horizontal') or rotation is None:
            return 0.
        elif cbook._str_equal(rotation, 'vertical'):
            return 90.
        else:
            raise ValueError("rotation is {!r}; expected either 'horizontal', "
                             "'vertical', numeric value, or None"
                             .format(rotation)) from err
