class Char(Node):
    """
    A single character.

    Unlike TeX, the font information and metrics are stored with each `Char`
    to make it easier to lookup the font metrics when needed.  Note that TeX
    boxes have a width, height, and depth, unlike Type1 and TrueType which use
    a full bounding box and an advance in the x-direction.  The metrics must
    be converted to the TeX model, and the advance (if different from width)
    must be converted into a `Kern` node when the `Char` is added to its parent
    `Hlist`.
    """

    def __init__(self, c, state, math=True):
        super().__init__()
        self.c = c
        self.font_output = state.font_output
        self.font = state.font
        self.font_class = state.font_class
        self.fontsize = state.fontsize
        self.dpi = state.dpi
        self.math = math
        # The real width, height and depth will be set during the
        # pack phase, after we know the real fontsize
        self._update_metrics()

    def __repr__(self):
        return '`%s`' % self.c

    def _update_metrics(self):
        metrics = self._metrics = self.font_output.get_metrics(
            self.font, self.font_class, self.c, self.fontsize, self.dpi,
            self.math)
        if self.c == ' ':
            self.width = metrics.advance
        else:
            self.width = metrics.width
        self.height = metrics.iceberg
        self.depth = -(metrics.iceberg - metrics.height)

    def is_slanted(self):
        return self._metrics.slanted

    def get_kerning(self, next):
        """
        Return the amount of kerning between this and the given character.

        This method is called when characters are strung together into `Hlist`
        to create `Kern` nodes.
        """
        advance = self._metrics.advance - self.width
        kern = 0.
        if isinstance(next, Char):
            kern = self.font_output.get_kern(
                self.font, self.font_class, self.c, self.fontsize,
                next.font, next.font_class, next.c, next.fontsize,
                self.dpi)
        return advance + kern

    def render(self, x, y):
        """
        Render the character to the canvas
        """
        self.font_output.render_glyph(
            x, y,
            self.font, self.font_class, self.c, self.fontsize, self.dpi)

    def shrink(self):
        super().shrink()
        if self.size < NUM_SIZE_LEVELS:
            self.fontsize *= SHRINK_FACTOR
            self.width    *= SHRINK_FACTOR
            self.height   *= SHRINK_FACTOR
            self.depth    *= SHRINK_FACTOR

    def grow(self):
        super().grow()
        self.fontsize *= GROW_FACTOR
        self.width    *= GROW_FACTOR
        self.height   *= GROW_FACTOR
        self.depth    *= GROW_FACTOR
