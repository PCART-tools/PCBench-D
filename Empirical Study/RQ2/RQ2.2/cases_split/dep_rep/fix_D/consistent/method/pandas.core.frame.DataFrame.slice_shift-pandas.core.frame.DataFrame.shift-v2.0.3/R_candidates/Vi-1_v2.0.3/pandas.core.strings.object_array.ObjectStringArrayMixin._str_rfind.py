    def _str_rfind(self, sub, start: int = 0, end=None):
        return self._str_find_(sub, start, end, side="right")
