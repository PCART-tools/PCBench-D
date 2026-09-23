    def _make_flip_transform(self, transform):
        return (transform +
                Affine2D()
                .scale(1.0, -1.0)
                .translate(0.0, self.height))
