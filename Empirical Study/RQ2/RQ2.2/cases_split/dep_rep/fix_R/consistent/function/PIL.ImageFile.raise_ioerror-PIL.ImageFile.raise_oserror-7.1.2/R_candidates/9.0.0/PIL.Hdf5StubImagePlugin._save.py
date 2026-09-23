def _save(im, fp, filename):
    if _handler is None or not hasattr("_handler", "save"):
        raise OSError("HDF5 save handler not installed")
    _handler.save(im, fp, filename)
