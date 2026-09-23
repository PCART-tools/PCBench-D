def load(file, *, encoding: str = "ASCII"):
    return Unpickler(file, encoding=encoding).load()
