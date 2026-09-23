class List(Box):
    """A list of nodes (either horizontal or vertical)."""

    def __init__(self, elements):
        super().__init__(0., 0., 0.)
        self.shift_amount = 0.   # An arbitrary offset
        self.children     = elements  # The child nodes of this list
        # The following parameters are set in the vpack and hpack functions
        self.glue_set     = 0.   # The glue setting of this list
        self.glue_sign    = 0    # 0: normal, -1: shrinking, 1: stretching
        self.glue_order   = 0    # The order of infinity (0 - 3) for the glue

    def __repr__(self):
        return '%s<w=%.02f h=%.02f d=%.02f s=%.02f>[%s]' % (
            super().__repr__(),
            self.width, self.height,
            self.depth, self.shift_amount,
            ', '.join([repr(x) for x in self.children]))

    def _set_glue(self, x, sign, totals, error_type):
        self.glue_order = o = next(
            # Highest order of glue used by the members of this list.
            (i for i in range(len(totals))[::-1] if totals[i] != 0), 0)
        self.glue_sign = sign
        if totals[o] != 0.:
            self.glue_set = x / totals[o]
        else:
            self.glue_sign = 0
            self.glue_ratio = 0.
        if o == 0:
            if len(self.children):
                _log.warning("%s %s: %r",
                             error_type, type(self).__name__, self)

    def shrink(self):
        for child in self.children:
            child.shrink()
        super().shrink()
        if self.size < NUM_SIZE_LEVELS:
            self.shift_amount *= SHRINK_FACTOR
            self.glue_set     *= SHRINK_FACTOR
