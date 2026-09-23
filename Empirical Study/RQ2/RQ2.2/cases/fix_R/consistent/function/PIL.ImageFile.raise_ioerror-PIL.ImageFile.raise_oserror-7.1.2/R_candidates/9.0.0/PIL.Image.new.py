def new(mode, size, color=0):
    """
    Creates a new image with the given mode and size.

    :param mode: The mode to use for the new image. See:
       :ref:`concept-modes`.
    :param size: A 2-tuple, containing (width, height) in pixels.
    :param color: What color to use for the image.  Default is black.
       If given, this should be a single integer or floating point value
       for single-band modes, and a tuple for multi-band modes (one value
       per band).  When creating RGB images, you can also use color
       strings as supported by the ImageColor module.  If the color is
       None, the image is not initialised.
    :returns: An :py:class:`~PIL.Image.Image` object.
    """

    _check_size(size)

    if color is None:
        # don't initialize
        return Image()._new(core.new(mode, size))

    if isinstance(color, str):
        # css3-style specifier

        from . import ImageColor

        color = ImageColor.getcolor(color, mode)

    im = Image()
    if mode == "P" and isinstance(color, (list, tuple)) and len(color) in [3, 4]:
        # RGB or RGBA value for a P image
        from . import ImagePalette

        im.palette = ImagePalette.ImagePalette()
        color = im.palette.getcolor(color)
    return im._new(core.fill(mode, size, color))
