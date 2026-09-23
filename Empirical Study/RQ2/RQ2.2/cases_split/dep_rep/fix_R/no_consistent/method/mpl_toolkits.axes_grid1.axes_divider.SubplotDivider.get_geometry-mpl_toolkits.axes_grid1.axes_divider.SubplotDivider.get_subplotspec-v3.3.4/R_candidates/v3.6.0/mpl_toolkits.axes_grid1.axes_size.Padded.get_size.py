    def get_size(self, renderer):
        r, a = self._size.get_size(renderer)
        rel_size = r
        abs_size = a + self._pad
        return rel_size, abs_size
