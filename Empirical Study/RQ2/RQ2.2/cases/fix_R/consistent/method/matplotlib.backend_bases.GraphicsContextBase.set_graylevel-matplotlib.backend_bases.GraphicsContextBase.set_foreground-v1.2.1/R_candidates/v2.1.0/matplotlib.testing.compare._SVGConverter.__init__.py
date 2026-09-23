    def __init__(self):
        self._proc = None
        # We cannot rely on the GC to trigger `__del__` at exit because
        # other modules (e.g. `subprocess`) may already have their globals
        # set to `None`, which make `proc.communicate` or `proc.terminate`
        # fail.  By relying on `atexit` we ensure the destructor runs before
        # `None`-setting occurs.
        atexit.register(self.__del__)
