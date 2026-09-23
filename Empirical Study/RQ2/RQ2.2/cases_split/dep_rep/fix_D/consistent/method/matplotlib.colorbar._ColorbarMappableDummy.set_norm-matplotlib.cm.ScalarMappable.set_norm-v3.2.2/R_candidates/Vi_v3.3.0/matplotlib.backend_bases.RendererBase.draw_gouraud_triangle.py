    def draw_gouraud_triangle(self, gc, points, colors, transform):
        """
        Draw a Gouraud-shaded triangle.

        Parameters
        ----------
        gc : `.GraphicsContextBase`
            The graphics context.

        points : array-like, shape=(3, 2)
            Array of (x, y) points for the triangle.

        colors : array-like, shape=(3, 4)
            RGBA colors for each point of the triangle.

        transform : `matplotlib.transforms.Transform`
            An affine transform to apply to the points.

        """
        raise NotImplementedError
