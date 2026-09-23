    def draw_gouraud_triangles(self, gc, triangles_array, colors_array,
                               transform):
        """
        Draws a series of Gouraud triangles.

        Parameters
        ----------
        points : array_like, shape=(N, 3, 2)
            Array of *N* (x, y) points for the triangles.

        colors : array_like, shape=(N, 3, 4)
            Array of *N* RGBA colors for each point of the triangles.

        transform : `matplotlib.transforms.Transform`
            An affine transform to apply to the points.
        """
        transform = transform.frozen()
        for tri, col in zip(triangles_array, colors_array):
            self.draw_gouraud_triangle(gc, tri, col, transform)
