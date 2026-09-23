def fromqimage(im):
    """
    :param im: QImage or PIL ImageQt object
    """
    buffer = QBuffer()
    if qt_version == "6":
        try:
            qt_openmode = QIODevice.OpenModeFlag
        except AttributeError:
            qt_openmode = QIODevice.OpenMode
    else:
        qt_openmode = QIODevice
    buffer.open(qt_openmode.ReadWrite)
    # preserve alpha channel with png
    # otherwise ppm is more friendly with Image.open
    if im.hasAlphaChannel():
        im.save(buffer, "png")
    else:
        im.save(buffer, "ppm")

    b = BytesIO()
    b.write(buffer.data())
    buffer.close()
    b.seek(0)

    return Image.open(b)
