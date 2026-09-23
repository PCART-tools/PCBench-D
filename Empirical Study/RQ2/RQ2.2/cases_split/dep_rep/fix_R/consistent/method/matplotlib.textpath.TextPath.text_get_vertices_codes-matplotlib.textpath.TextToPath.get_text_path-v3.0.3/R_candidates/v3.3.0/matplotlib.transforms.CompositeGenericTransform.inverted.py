    def inverted(self):
        # docstring inherited
        return CompositeGenericTransform(
            self._b.inverted(), self._a.inverted())
