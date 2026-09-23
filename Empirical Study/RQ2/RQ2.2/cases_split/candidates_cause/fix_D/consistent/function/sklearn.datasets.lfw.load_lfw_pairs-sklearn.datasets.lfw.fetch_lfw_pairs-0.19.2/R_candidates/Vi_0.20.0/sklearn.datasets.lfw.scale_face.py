@deprecated('This function was deprecated in version 0.20 and will be removed '
            'in 0.22.')
def scale_face(face):
    """Scale back to 0-1 range in case of normalization for plotting.

    .. deprecated:: 0.20
    This function was deprecated in version 0.20 and will be removed in 0.22.


    Parameters
    ----------
    face : array_like
        The array to scale

    Returns
    -------
    array_like
        The scaled array
    """
    scaled = face - face.min()
    scaled /= scaled.max()
    return scaled
