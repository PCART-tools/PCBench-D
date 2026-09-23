    def get_trifinder(self):
        """
        Return the default `matplotlib.tri.TriFinder` of this
        triangulation, creating it if necessary.  This allows the same
        TriFinder object to be easily shared.
        """
        if self._trifinder is None:
            # Default TriFinder class.
            from matplotlib.tri.trifinder import TrapezoidMapTriFinder
            self._trifinder = TrapezoidMapTriFinder(self)
        return self._trifinder
