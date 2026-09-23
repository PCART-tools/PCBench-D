    def remove(self):
        for c in cbook.flatten(
                self, scalarp=lambda x: isinstance(x, Artist)):
            if c is not None:
                c.remove()

        if self._remove_method:
            self._remove_method(self)
