def raise_ioerror(error):
    try:
        message = Image.core.getcodecstatus(error)
    except AttributeError:
        message = ERRORS.get(error)
    if not message:
        message = "decoder error %d" % error
    raise OSError(message + " when reading image file")
