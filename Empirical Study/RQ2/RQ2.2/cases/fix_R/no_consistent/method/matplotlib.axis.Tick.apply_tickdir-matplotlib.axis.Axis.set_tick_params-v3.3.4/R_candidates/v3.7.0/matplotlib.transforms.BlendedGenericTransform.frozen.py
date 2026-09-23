    def frozen(self):
        # docstring inherited
        return blended_transform_factory(self._x.frozen(), self._y.frozen())
