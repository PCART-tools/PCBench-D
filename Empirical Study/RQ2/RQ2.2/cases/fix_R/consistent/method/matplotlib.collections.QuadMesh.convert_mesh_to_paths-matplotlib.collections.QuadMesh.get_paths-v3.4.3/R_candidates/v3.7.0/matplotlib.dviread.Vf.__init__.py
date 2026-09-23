    def __init__(self, filename):
        super().__init__(filename, 0)
        try:
            self._first_font = None
            self._chars = {}
            self._read()
        finally:
            self.close()
