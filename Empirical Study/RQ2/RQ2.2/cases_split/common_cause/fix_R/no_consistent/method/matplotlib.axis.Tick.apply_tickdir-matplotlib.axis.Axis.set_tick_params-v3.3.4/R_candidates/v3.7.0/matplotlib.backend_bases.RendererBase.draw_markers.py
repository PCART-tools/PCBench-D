    def draw_markers(self, gc, marker_path, marker_trans, path,
                     trans, rgbFace=None):
        """
        Draw a marker at each of *path*'s vertices (excluding control points).

        The base (fallback) implementation makes multiple calls to `draw_path`.
        Backends may want to override this method in order to draw the marker
        only once and reuse it multiple times.

        Parameters
        ----------
        gc : `.GraphicsContextBase`
            The graphics context.
        marker_trans : `matplotlib.transforms.Transform`
            An affine transform applied to the marker.
        trans : `matplotlib.transforms.Transform`
            An affine transform applied to the path.
        """
        for vertices, codes in path.iter_segments(trans, simplify=False):
            if len(vertices):
                x, y = vertices[-2:]
                self.draw_path(gc, marker_path,
                               marker_trans +
                               transforms.Affine2D().translate(x, y),
                               rgbFace)
