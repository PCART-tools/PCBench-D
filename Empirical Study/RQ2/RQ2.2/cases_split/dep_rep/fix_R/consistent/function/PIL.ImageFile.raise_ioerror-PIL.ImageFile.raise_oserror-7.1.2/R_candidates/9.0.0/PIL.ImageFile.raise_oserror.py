def raise_oserror(error):
    try:
        message = Image.core.getcodecstatus(error)
    except AttributeError:
        message = ERRORS.get(error)
    if not message:
        message = f"decoder error {error}"
    raise OSError(message + " when reading image file")
