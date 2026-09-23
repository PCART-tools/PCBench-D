    def inverted(self):
        # docstring inherited
        return BlendedGenericTransform(self._x.inverted(), self._y.inverted())
