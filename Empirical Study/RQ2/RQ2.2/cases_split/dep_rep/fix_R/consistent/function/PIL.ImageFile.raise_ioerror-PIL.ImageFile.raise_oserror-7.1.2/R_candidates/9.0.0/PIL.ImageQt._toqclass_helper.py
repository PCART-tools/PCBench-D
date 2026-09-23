def _toqclass_helper(im):
    data = None
    colortable = None
    exclusive_fp = False

    # handle filename, if given instead of image name
    if hasattr(im, "toUtf8"):
        # FIXME - is this really the best way to do this?
        im = str(im.toUtf8(), "utf-8")
    if isPath(im):
        im = Image.open(im)
        exclusive_fp = True

    qt_format = QImage.Format if qt_version == "6" else QImage
    if im.mode == "1":
        format = qt_format.Format_Mono
    elif im.mode == "L":
        format = qt_format.Format_Indexed8
        colortable = []
        for i in range(256):
            colortable.append(rgb(i, i, i))
    elif im.mode == "P":
        format = qt_format.Format_Indexed8
        colortable = []
        palette = im.getpalette()
        for i in range(0, len(palette), 3):
            colortable.append(rgb(*palette[i : i + 3]))
    elif im.mode == "RGB":
        # Populate the 4th channel with 255
        im = im.convert("RGBA")

        data = im.tobytes("raw", "BGRA")
        format = qt_format.Format_RGB32
    elif im.mode == "RGBA":
        data = im.tobytes("raw", "BGRA")
        format = qt_format.Format_ARGB32
    elif im.mode == "I;16" and hasattr(qt_format, "Format_Grayscale16"):  # Qt 5.13+
        im = im.point(lambda i: i * 256)

        format = qt_format.Format_Grayscale16
    else:
        if exclusive_fp:
            im.close()
        raise ValueError(f"unsupported image mode {repr(im.mode)}")

    size = im.size
    __data = data or align8to32(im.tobytes(), size[0], im.mode)
    if exclusive_fp:
        im.close()
    return {"data": __data, "size": size, "format": format, "colortable": colortable}
