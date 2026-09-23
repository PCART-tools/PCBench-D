    def _make_flip_transform(self, transform):
        return transform + Affine2D().scale(1, -1).translate(0, self.height)
