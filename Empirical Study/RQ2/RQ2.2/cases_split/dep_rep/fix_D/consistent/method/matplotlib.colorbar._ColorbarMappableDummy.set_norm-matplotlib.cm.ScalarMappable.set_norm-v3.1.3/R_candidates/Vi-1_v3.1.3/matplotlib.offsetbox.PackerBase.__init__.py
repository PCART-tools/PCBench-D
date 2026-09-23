    def __init__(self, pad=None, sep=None, width=None, height=None,
                 align=None, mode=None,
                 children=None):
        """
        Parameters
        ----------
        pad : float, optional
            The boundary padding in points.

        sep : float, optional
            The spacing between items in points.

        width, height : float, optional
            Width and height of the container box in pixels, calculated if
            *None*.

        align : {'top', 'bottom', 'left', 'right', 'center', 'baseline'}
            Alignment of boxes.

        mode : {'fixed', 'expand', 'equal'}
            The packing mode.

            - 'fixed' packs the given `.Artists` tight with *sep* spacing.
            - 'expand' uses the maximal available space to distribute the
              artists with equal spacing in between.
            - 'equal': Each artist an equal fraction of the available space
              and is left-aligned (or top-aligned) therein.

        children : list of `.Artist`
            The artists to pack.

        Notes
        -----
        *pad* and *sep* need to given in points and will be scale with
        the renderer dpi, while *width* and *height* need to be in
        pixels.
        """
        super().__init__()

        self.height = height
        self.width = width
        self.sep = sep
        self.pad = pad
        self.mode = mode
        self.align = align

        self._children = children
