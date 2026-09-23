    def hpack(self, w=0., m='additional'):
        """
        The main duty of :meth:`hpack` is to compute the dimensions of
        the resulting boxes, and to adjust the glue if one of those
        dimensions is pre-specified.  The computed sizes normally
        enclose all of the material inside the new box; but some items
        may stick out if negative glue is used, if the box is
        overfull, or if a ``\\vbox`` includes other boxes that have
        been shifted left.

          - *w*: specifies a width

          - *m*: is either 'exactly' or 'additional'.

        Thus, ``hpack(w, 'exactly')`` produces a box whose width is
        exactly *w*, while ``hpack(w, 'additional')`` yields a box
        whose width is the natural width plus *w*.  The default values
        produce a box with the natural width.
        """
        # I don't know why these get reset in TeX.  Shift_amount is pretty
        # much useless if we do.
        #self.shift_amount = 0.
        h = 0.
        d = 0.
        x = 0.
        total_stretch = [0.] * 4
        total_shrink = [0.] * 4
        for p in self.children:
            if isinstance(p, Char):
                x += p.width
                h = max(h, p.height)
                d = max(d, p.depth)
            elif isinstance(p, Box):
                x += p.width
                if not np.isinf(p.height) and not np.isinf(p.depth):
                    s = getattr(p, 'shift_amount', 0.)
                    h = max(h, p.height - s)
                    d = max(d, p.depth + s)
            elif isinstance(p, Glue):
                glue_spec = p.glue_spec
                x += glue_spec.width
                total_stretch[glue_spec.stretch_order] += glue_spec.stretch
                total_shrink[glue_spec.shrink_order] += glue_spec.shrink
            elif isinstance(p, Kern):
                x += p.width
        self.height = h
        self.depth = d

        if m == 'additional':
            w += x
        self.width = w
        x = w - x

        if x == 0.:
            self.glue_sign = 0
            self.glue_order = 0
            self.glue_ratio = 0.
            return
        if x > 0.:
            self._set_glue(x, 1, total_stretch, "Overfull")
        else:
            self._set_glue(x, -1, total_shrink, "Underfull")
