    def _get_rotation_transform(self):
        aspect_ratio = self.ax._get_aspect_ratio()
        return Affine2D().translate(-self.center[0], -self.center[1]) \
                .scale(1, aspect_ratio) \
                .rotate(self._rotation) \
                .scale(1, 1 / aspect_ratio) \
                .translate(*self.center)
