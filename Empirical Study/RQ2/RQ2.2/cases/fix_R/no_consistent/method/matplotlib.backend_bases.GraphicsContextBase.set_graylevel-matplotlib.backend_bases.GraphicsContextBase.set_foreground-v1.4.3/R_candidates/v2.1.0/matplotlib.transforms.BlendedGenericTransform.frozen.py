    def frozen(self):
        return blended_transform_factory(self._x.frozen(), self._y.frozen())
