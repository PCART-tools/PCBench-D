def load_path(filename):
    """
    Load font file. Same as :py:func:`~PIL.ImageFont.load`, but searches for a
    bitmap font along the Python path.

    :param filename: Name of font file.
    :return: A font object.
    :exception OSError: If the file could not be read.
    """
    for directory in sys.path:
        if isDirectory(directory):
            if not isinstance(filename, str):
                filename = filename.decode("utf-8")
            try:
                return load(os.path.join(directory, filename))
            except OSError:
                pass
    raise OSError("cannot find font file")
