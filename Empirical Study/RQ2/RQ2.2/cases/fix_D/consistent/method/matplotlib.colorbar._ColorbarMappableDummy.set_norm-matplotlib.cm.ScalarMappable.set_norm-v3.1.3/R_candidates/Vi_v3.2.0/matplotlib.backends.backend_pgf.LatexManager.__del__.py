    def __del__(self):
        _log.debug("deleting LatexManager")
        self._cleanup()
