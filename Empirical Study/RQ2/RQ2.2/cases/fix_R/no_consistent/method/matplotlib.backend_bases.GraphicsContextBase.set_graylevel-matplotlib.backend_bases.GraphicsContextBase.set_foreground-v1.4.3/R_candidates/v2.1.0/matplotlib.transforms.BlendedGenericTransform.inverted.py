    def inverted(self):
        return BlendedGenericTransform(self._x.inverted(), self._y.inverted())
