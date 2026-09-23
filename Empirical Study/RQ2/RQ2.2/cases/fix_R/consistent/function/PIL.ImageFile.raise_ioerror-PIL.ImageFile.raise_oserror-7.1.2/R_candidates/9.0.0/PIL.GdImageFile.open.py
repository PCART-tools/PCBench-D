def open(fp, mode="r"):
    """
    Load texture from a GD image file.

    :param filename: GD file name, or an opened file handle.
    :param mode: Optional mode.  In this version, if the mode argument
        is given, it must be "r".
    :returns: An image instance.
    :raises OSError: If the image could not be read.
    """
    if mode != "r":
        raise ValueError("bad mode")

    try:
        return GdImageFile(fp)
    except SyntaxError as e:
        raise UnidentifiedImageError("cannot identify this image file") from e
