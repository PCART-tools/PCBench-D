    def draw_gouraud_triangles(self, gc, triangles_array, colors_array,
                               transform):
        """
        Draw a series of Gouraud triangles.

        Parameters
        ----------
        gc : `.GraphicsContextBase`
            The graphics context.
        triangles_array : (N, 3, 2) array-like
            Array of *N* (x, y) points for the triangles.
        colors_array : (N, 3, 4) array-like
            Array of *N* RGBA colors for each point of the triangles.
        transform : `~matplotlib.transforms.Transform`
            An affine transform to apply to the points.
        """
        raise NotImplementedError
