    def __init__(self, filename):
        Dvi.__init__(self, filename, 0)
        try:
            self._first_font = None
            self._chars = {}
            self._read()
        finally:
            self.close()
