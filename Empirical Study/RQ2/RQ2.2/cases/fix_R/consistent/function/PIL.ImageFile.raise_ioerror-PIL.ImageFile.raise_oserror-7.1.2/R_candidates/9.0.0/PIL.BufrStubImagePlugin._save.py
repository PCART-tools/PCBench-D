def _save(im, fp, filename):
    if _handler is None or not hasattr("_handler", "save"):
        raise OSError("BUFR save handler not installed")
    _handler.save(im, fp, filename)
