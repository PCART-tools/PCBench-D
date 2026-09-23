def open(fp, mode="r", formats=None):
    """
    Opens and identifies the given image file.

    This is a lazy operation; this function identifies the file, but
    the file remains open and the actual image data is not read from
    the file until you try to process the data (or call the
    :py:meth:`~PIL.Image.Image.load` method).  See
    :py:func:`~PIL.Image.new`. See :ref:`file-handling`.

    :param fp: A filename (string), pathlib.Path object or a file object.
       The file object must implement ``file.read``,
       ``file.seek``, and ``file.tell`` methods,
       and be opened in binary mode.
    :param mode: The mode.  If given, this argument must be "r".
    :param formats: A list or tuple of formats to attempt to load the file in.
       This can be used to restrict the set of formats checked.
       Pass ``None`` to try all supported formats. You can print the set of
       available formats by running ``python3 -m PIL`` or using
       the :py:func:`PIL.features.pilinfo` function.
    :returns: An :py:class:`~PIL.Image.Image` object.
    :exception FileNotFoundError: If the file cannot be found.
    :exception PIL.UnidentifiedImageError: If the image cannot be opened and
       identified.
    :exception ValueError: If the ``mode`` is not "r", or if a ``StringIO``
       instance is used for ``fp``.
    :exception TypeError: If ``formats`` is not ``None``, a list or a tuple.
    """

    if mode != "r":
        raise ValueError(f"bad mode {repr(mode)}")
    elif isinstance(fp, io.StringIO):
        raise ValueError(
            "StringIO cannot be used to open an image. "
            "Binary data must be used instead."
        )

    if formats is None:
        formats = ID
    elif not isinstance(formats, (list, tuple)):
        raise TypeError("formats must be a list or tuple")

    exclusive_fp = False
    filename = ""
    if isinstance(fp, Path):
        filename = str(fp.resolve())
    elif isPath(fp):
        filename = fp

    if filename:
        fp = builtins.open(filename, "rb")
        exclusive_fp = True

    try:
        fp.seek(0)
    except (AttributeError, io.UnsupportedOperation):
        fp = io.BytesIO(fp.read())
        exclusive_fp = True

    prefix = fp.read(16)

    preinit()

    accept_warnings = []

    def _open_core(fp, filename, prefix, formats):
        for i in formats:
            i = i.upper()
            if i not in OPEN:
                init()
            try:
                factory, accept = OPEN[i]
                result = not accept or accept(prefix)
                if type(result) in [str, bytes]:
                    accept_warnings.append(result)
                elif result:
                    fp.seek(0)
                    im = factory(fp, filename)
                    _decompression_bomb_check(im.size)
                    return im
            except (SyntaxError, IndexError, TypeError, struct.error):
                # Leave disabled by default, spams the logs with image
                # opening failures that are entirely expected.
                # logger.debug("", exc_info=True)
                continue
            except BaseException:
                if exclusive_fp:
                    fp.close()
                raise
        return None

    im = _open_core(fp, filename, prefix, formats)

    if im is None:
        if init():
            im = _open_core(fp, filename, prefix, formats)

    if im:
        im._exclusive_fp = exclusive_fp
        return im

    if exclusive_fp:
        fp.close()
    for message in accept_warnings:
        warnings.warn(message)
    raise UnidentifiedImageError(
        "cannot identify image file %r" % (filename if filename else fp)
    )
