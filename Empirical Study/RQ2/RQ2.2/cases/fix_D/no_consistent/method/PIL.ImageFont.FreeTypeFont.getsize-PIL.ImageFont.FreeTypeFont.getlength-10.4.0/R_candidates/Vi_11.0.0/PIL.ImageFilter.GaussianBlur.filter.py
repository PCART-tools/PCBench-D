    def filter(self, image: _imaging.ImagingCore) -> _imaging.ImagingCore:
        xy = self.radius
        if isinstance(xy, (int, float)):
            xy = (xy, xy)
        if xy == (0, 0):
            return image.copy()
        return image.gaussian_blur(xy)
