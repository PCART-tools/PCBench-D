class RemoteException(Exception):
    """ Remote Exception

    Contains the exception and traceback from a remotely run task
    """
    def __init__(self, exception, traceback):
        self.exception = exception
        self.traceback = traceback

    def __str__(self):
        return (str(self.exception) + "\n\n"
                "Traceback\n"
                "---------\n" +
                self.traceback)

    def __dir__(self):
        return sorted(set(dir(type(self)) +
                      list(self.__dict__) +
                      dir(self.exception)))

    def __getattr__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            return getattr(self.exception, key)
