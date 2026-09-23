    class SquareCollection(mcollections.RegularPolyCollection):
        def __init__(self, **kwargs):
            super().__init__(4, rotation=np.pi/4., **kwargs)

        def get_transform(self):
            """Return transform scaling circle areas to data space."""
            ax = self.axes

            pts2pixels = 72.0 / ax.figure.dpi

            scale_x = pts2pixels * ax.bbox.width / ax.viewLim.width
            scale_y = pts2pixels * ax.bbox.height / ax.viewLim.height
            return mtransforms.Affine2D().scale(scale_x, scale_y)
