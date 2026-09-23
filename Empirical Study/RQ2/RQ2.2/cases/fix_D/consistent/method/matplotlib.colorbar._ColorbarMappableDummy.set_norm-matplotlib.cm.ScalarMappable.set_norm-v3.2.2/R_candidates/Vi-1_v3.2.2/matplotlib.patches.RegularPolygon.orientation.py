    @orientation.setter
    def orientation(self, orientation):
        self._orientation = orientation
        self._update_transform()
