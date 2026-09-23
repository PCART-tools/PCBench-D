    @_docstring.dedent_interpd
    @_api.make_keyword_only("3.6", name="width")
    def __init__(self, x, y, dx, dy, width=1.0, **kwargs):
        """
        Draws an arrow from (*x*, *y*) to (*x* + *dx*, *y* + *dy*).
        The width of the arrow is scaled by *width*.

        Parameters
        ----------
        x : float
            x coordinate of the arrow tail.
        y : float
            y coordinate of the arrow tail.
        dx : float
            Arrow length in the x direction.
        dy : float
            Arrow length in the y direction.
        width : float, default: 1
            Scale factor for the width of the arrow. With a default value of 1,
            the tail width is 0.2 and head width is 0.6.
        **kwargs
            Keyword arguments control the `Patch` properties:

            %(Patch:kwdoc)s

        See Also
        --------
        FancyArrow
            Patch that allows independent control of the head and tail
            properties.
        """
        super().__init__(**kwargs)
        self._patch_transform = (
            transforms.Affine2D()
            .scale(np.hypot(dx, dy), width)
            .rotate(np.arctan2(dy, dx))
            .translate(x, y)
            .frozen())
