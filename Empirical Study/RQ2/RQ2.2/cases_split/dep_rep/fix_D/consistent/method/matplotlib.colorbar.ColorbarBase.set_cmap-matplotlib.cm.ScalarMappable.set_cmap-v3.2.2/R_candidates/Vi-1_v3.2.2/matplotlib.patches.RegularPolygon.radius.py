    @radius.setter
    def radius(self, radius):
        self._radius = radius
        self._update_transform()
