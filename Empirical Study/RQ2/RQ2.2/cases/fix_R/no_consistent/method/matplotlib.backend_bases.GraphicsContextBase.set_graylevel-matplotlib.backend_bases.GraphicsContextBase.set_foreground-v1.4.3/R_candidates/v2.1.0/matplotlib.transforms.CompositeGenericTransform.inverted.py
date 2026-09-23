    def inverted(self):
        return CompositeGenericTransform(self._b.inverted(), self._a.inverted())
