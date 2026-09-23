    def _get_affine_transform(self):
        return Affine2D() \
            .scale(0.25) \
            .translate(0.5, 0.5)
