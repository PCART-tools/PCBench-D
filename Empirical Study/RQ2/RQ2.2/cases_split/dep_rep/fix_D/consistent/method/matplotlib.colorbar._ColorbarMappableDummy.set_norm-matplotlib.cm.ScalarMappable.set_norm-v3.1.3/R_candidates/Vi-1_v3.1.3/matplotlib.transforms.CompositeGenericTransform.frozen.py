    def frozen(self):
        # docstring inherited
        self._invalid = 0
        frozen = composite_transform_factory(self._a.frozen(), self._b.frozen())
        if not isinstance(frozen, CompositeGenericTransform):
            return frozen.frozen()
        return frozen
