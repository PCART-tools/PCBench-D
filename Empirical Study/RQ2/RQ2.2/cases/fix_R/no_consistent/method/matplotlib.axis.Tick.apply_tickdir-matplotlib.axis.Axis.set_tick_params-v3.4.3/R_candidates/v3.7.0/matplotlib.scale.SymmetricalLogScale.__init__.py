    def __init__(self, axis, *, base=10, linthresh=2, subs=None, linscale=1):
        self._transform = SymmetricalLogTransform(base, linthresh, linscale)
        self.subs = subs
