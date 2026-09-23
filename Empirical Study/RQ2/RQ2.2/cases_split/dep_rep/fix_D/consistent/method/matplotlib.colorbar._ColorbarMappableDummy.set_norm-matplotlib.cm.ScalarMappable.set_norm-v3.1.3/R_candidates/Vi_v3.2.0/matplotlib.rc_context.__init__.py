    def __init__(self, rc=None, fname=None):
        self._orig = rcParams.copy()
        try:
            if fname:
                rc_file(fname)
            if rc:
                rcParams.update(rc)
        except Exception:
            self.__fallback()
            raise
