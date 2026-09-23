    def inverted(self):
        return FuncTransform(self._inverse, self._forward)
