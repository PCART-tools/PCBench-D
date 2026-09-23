    def set_patch_circle(self, center, radius):
        """set the spine to be circular"""
        self._patch_type = 'circle'
        self._center = center
        self._width = radius * 2
        self._height = radius * 2
        # circle drawn on axes transform
        self.set_transform(self.axes.transAxes)
        self.stale = True
