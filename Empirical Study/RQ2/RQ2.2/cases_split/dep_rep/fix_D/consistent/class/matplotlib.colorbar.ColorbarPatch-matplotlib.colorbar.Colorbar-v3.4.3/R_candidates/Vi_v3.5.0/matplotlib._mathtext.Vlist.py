class Vlist(List):
    """A vertical list of boxes."""

    def __init__(self, elements, h=0., m='additional'):
        super().__init__(elements)
        self.vpack()

    def vpack(self, h=0., m='additional', l=np.inf):
        """
        Compute the dimensions of the resulting boxes, and to adjust the glue
        if one of those dimensions is pre-specified.

        Parameters
        ----------
        h : float, default: 0
            A height.
        m : {'exactly', 'additional'}, default: 'additional'
            Whether to produce a box whose height is 'exactly' *w*; or a box
            with the natural height of the contents, plus *w* ('additional').
        l : float, default: np.inf
            The maximum height.

        Notes
        -----
        The defaults produce a box with the natural height of the contents.
        """
        # I don't know why these get reset in TeX.  Shift_amount is pretty
        # much useless if we do.
        # self.shift_amount = 0.
        w = 0.
        d = 0.
        x = 0.
        total_stretch = [0.] * 4
        total_shrink = [0.] * 4
        for p in self.children:
            if isinstance(p, Box):
                x += d + p.height
                d = p.depth
                if not np.isinf(p.width):
                    s = getattr(p, 'shift_amount', 0.)
                    w = max(w, p.width + s)
            elif isinstance(p, Glue):
                x += d
                d = 0.
                glue_spec = p.glue_spec
                x += glue_spec.width
                total_stretch[glue_spec.stretch_order] += glue_spec.stretch
                total_shrink[glue_spec.shrink_order] += glue_spec.shrink
            elif isinstance(p, Kern):
                x += d + p.width
                d = 0.
            elif isinstance(p, Char):
                raise RuntimeError(
                    "Internal mathtext error: Char node found in Vlist")

        self.width = w
        if d > l:
            x += d - l
            self.depth = l
        else:
            self.depth = d

        if m == 'additional':
            h += x
        self.height = h
        x = h - x

        if x == 0:
            self.glue_sign = 0
            self.glue_order = 0
            self.glue_ratio = 0.
            return

        if x > 0.:
            self._set_glue(x, 1, total_stretch, "Overfull")
        else:
            self._set_glue(x, -1, total_shrink, "Underfull")
