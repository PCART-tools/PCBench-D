def merge(mode, bands):
    """
    Merge a set of single band images into a new multiband image.

    :param mode: The mode to use for the output image. See:
        :ref:`concept-modes`.
    :param bands: A sequence containing one single-band image for
        each band in the output image.  All bands must have the
        same size.
    :returns: An :py:class:`~PIL.Image.Image` object.
    """

    if getmodebands(mode) != len(bands) or "*" in mode:
        raise ValueError("wrong number of bands")
    for band in bands[1:]:
        if band.mode != getmodetype(mode):
            raise ValueError("mode mismatch")
        if band.size != bands[0].size:
            raise ValueError("size mismatch")
    for band in bands:
        band.load()
    return bands[0]._new(core.merge(mode, *[b.im for b in bands]))
