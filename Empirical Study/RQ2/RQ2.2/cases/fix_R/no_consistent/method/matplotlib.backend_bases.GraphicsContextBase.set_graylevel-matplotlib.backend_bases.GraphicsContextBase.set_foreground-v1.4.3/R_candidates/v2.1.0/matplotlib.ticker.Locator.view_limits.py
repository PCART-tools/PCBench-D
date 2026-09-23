    def view_limits(self, vmin, vmax):
        """
        select a scale for the range from vmin to vmax

        Normally this method is overridden by subclasses to
        change locator behaviour.
        """
        return mtransforms.nonsingular(vmin, vmax)
