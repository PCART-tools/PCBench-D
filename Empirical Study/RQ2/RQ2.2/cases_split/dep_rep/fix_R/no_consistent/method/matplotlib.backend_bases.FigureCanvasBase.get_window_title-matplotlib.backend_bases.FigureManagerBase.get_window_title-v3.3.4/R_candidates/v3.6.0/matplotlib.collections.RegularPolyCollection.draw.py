    @artist.allow_rasterization
    def draw(self, renderer):
        self.set_sizes(self._sizes, self.figure.dpi)
        self._transforms = [
            transforms.Affine2D(x).rotate(-self._rotation).get_matrix()
            for x in self._transforms
        ]
        # Explicitly not super().draw, because set_sizes must be called before
        # updating self._transforms.
        Collection.draw(self, renderer)
