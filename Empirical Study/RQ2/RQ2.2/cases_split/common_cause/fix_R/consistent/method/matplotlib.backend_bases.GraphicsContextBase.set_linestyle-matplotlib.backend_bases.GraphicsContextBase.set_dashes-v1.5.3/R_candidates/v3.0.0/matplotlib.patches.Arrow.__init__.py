    @docstring.dedent_interpd
    def __init__(self, x, y, dx, dy, width=1.0, **kwargs):
        """
        Draws an arrow from (*x*, *y*) to (*x* + *dx*, *y* + *dy*).
        The width of the arrow is scaled by *width*.

        Parameters
        ----------
        x : scalar
            x coordinate of the arrow tail
        y : scalar
            y coordinate of the arrow tail
        dx : scalar
            Arrow length in the x direction
        dy : scalar
            Arrow length in the y direction
        width : scalar, optional (default: 1)
            Scale factor for the width of the arrow. With a default value of
            1, the tail width is 0.2 and head width is 0.6.
        **kwargs :
            Keyword arguments control the :class:`~matplotlib.patches.Patch`
            properties:

            %(Patch)s

        See Also
        --------
        :class:`FancyArrow` :
            Patch that allows independent control of the head and tail
            properties
        """
        Patch.__init__(self, **kwargs)
        L = np.hypot(dx, dy)

        if L != 0:
            cx = dx / L
            sx = dy / L
        else:
            # Account for division by zero
            cx, sx = 0, 1

        trans1 = transforms.Affine2D().scale(L, width)
        trans2 = transforms.Affine2D.from_values(cx, sx, -sx, cx, 0.0, 0.0)
        trans3 = transforms.Affine2D().translate(x, y)
        trans = trans1 + trans2 + trans3
        self._patch_transform = trans.frozen()
