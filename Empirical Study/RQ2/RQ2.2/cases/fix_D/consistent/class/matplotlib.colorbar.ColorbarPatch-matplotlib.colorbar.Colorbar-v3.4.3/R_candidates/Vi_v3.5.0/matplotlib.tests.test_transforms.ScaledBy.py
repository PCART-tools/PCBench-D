    class ScaledBy:
        def __init__(self, scale_factor):
            self._scale_factor = scale_factor

        def _as_mpl_transform(self, axes):
            return (mtransforms.Affine2D().scale(self._scale_factor)
                    + axes.transData)
