    def set_clim(self, vmin=None, vmax=None):
        """
        set the norm limits for image scaling; if *vmin* is a length2
        sequence, interpret it as ``(vmin, vmax)`` which is used to
        support setp

        ACCEPTS: a length 2 sequence of floats; may be overridden in methods
        that have ``vmin`` and ``vmax`` kwargs.
        """
        if vmax is None:
            try:
                vmin, vmax = vmin
            except (TypeError, ValueError):
                pass
        if vmin is not None:
            self.norm.vmin = colors._sanitize_extrema(vmin)
        if vmax is not None:
            self.norm.vmax = colors._sanitize_extrema(vmax)
        self.changed()
