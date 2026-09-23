    def __init__(self, pad=None, sep=None, width=None, height=None,
                 align=None, mode=None,
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
           Width and height of the container box, calculated if
           `None`.

        align : str, optional
            Alignment of boxes. Can be one of ``top``, ``bottom``,
            ``left``, ``right``, ``center`` and ``baseline``

        mode : str, optional
            Packing mode.

        Notes
        -----
        *pad* and *sep* need to given in points and will be scale with
        the renderer dpi, while *width* and *height* need to be in
        pixels.
        """
        super(PackerBase, self).__init__()

        self.height = height
        self.width = width
        self.sep = sep
        self.pad = pad
        self.mode = mode
        self.align = align

        self._children = children
