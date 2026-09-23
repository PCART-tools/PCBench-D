    def __del__(self):
        if self._debug:
            print("deleting LatexManager")
        self._cleanup()
