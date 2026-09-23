def fromarray(obj, mode=None):
    """
    Creates an image memory from an object exporting the array interface
    (using the buffer protocol).

    If ``obj`` is not contiguous, then the ``tobytes`` method is called
    and :py:func:`~PIL.Image.frombuffer` is used.

    If you have an image in NumPy::

      from PIL import Image
      import numpy as np
      im = Image.open("hopper.jpg")
      a = np.asarray(im)

    Then this can be used to convert it to a Pillow image::

      im = Image.fromarray(a)

    :param obj: Object with array interface
    :param mode: Optional mode to use when reading ``obj``. Will be determined from
      type if ``None``.

      This will not be used to convert the data after reading, but will be used to
      change how the data is read::

        from PIL import Image
        import numpy as np
        a = np.full((1, 1), 300)
        im = Image.fromarray(a, mode="L")
        im.getpixel((0, 0))  # 44
        im = Image.fromarray(a, mode="RGB")
        im.getpixel((0, 0))  # (44, 1, 0)

      See: :ref:`concept-modes` for general information about modes.
    :returns: An image object.

    .. versionadded:: 1.1.6
    """
    arr = obj.__array_interface__
    shape = arr["shape"]
    ndim = len(shape)
    strides = arr.get("strides", None)
    if mode is None:
        try:
            typekey = (1, 1) + shape[2:], arr["typestr"]
        except KeyError as e:
            raise TypeError("Cannot handle this data type") from e
        try:
            mode, rawmode = _fromarray_typemap[typekey]
        except KeyError as e:
            raise TypeError("Cannot handle this data type: %s, %s" % typekey) from e
    else:
        rawmode = mode
    if mode in ["1", "L", "I", "P", "F"]:
        ndmax = 2
    elif mode == "RGB":
        ndmax = 3
    else:
        ndmax = 4
    if ndim > ndmax:
        raise ValueError(f"Too many dimensions: {ndim} > {ndmax}.")

    size = 1 if ndim == 1 else shape[1], shape[0]
    if strides is not None:
        if hasattr(obj, "tobytes"):
            obj = obj.tobytes()
        else:
            obj = obj.tostring()

    return frombuffer(mode, size, obj, "raw", rawmode, 0, 1)
