def scale(image, factor, resample=Image.BICUBIC):
    """
    Returns a rescaled image by a specific factor given in parameter.
    A factor greater than 1 expands the image, between 0 and 1 contracts the
    image.

    :param image: The image to rescale.
    :param factor: The expansion factor, as a float.
    :param resample: Resampling method to use. Default is
                     :py:attr:`PIL.Image.BICUBIC`. See :ref:`concept-filters`.
    :returns: An :py:class:`~PIL.Image.Image` object.
    """
    if factor == 1:
        return image.copy()
    elif factor <= 0:
        raise ValueError("the factor must be greater than 0")
    else:
        size = (round(factor * image.width), round(factor * image.height))
        return image.resize(size, resample)
