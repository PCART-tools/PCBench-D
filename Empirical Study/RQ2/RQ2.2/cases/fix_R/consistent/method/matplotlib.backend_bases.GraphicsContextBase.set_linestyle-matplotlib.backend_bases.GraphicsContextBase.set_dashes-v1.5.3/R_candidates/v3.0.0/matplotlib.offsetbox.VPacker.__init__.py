    def __init__(self, pad=None, sep=None, width=None, height=None,
                 align="baseline", mode="fixed",
                 children=None):
        """
        Parameters
        ----------
        pad : float, optional
            Boundary pad.

        sep : float, optional
            Spacing between items.

        width : float, optional

        height : float, optional

            width and height of the container box, calculated if
            `None`.

        align : str, optional
            Alignment of boxes.

        mode : str, optional
            Packing mode.

        Notes
        -----
        *pad* and *sep* need to given in points and will be scale with
        the renderer dpi, while *width* and *height* need to be in
        pixels.
        """
        super().__init__(pad, sep, width, height, align, mode, children)
