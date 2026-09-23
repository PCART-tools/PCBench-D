    def set_transform(self, t):
        # docstring inherited
        self._invalidx = True
        self._invalidy = True
        super().set_transform(t)
