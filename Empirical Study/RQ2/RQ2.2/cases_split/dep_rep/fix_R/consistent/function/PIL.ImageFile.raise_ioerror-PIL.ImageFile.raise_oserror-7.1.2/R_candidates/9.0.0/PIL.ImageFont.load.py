def load(filename):
    """
    Load a font file.  This function loads a font object from the given
    bitmap font file, and returns the corresponding font object.

    :param filename: Name of font file.
    :return: A font object.
    :exception OSError: If the file could not be read.
    """
    f = ImageFont()
    f._load_pilfont(filename)
    return f
