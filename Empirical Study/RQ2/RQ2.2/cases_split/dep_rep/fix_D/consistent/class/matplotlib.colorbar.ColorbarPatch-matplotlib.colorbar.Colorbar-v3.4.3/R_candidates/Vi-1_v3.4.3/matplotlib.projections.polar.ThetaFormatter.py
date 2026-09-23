class ThetaFormatter(mticker.Formatter):
    """
    Used to format the *theta* tick labels.  Converts the native
    unit of radians into degrees and adds a degree symbol.
    """
    def __call__(self, x, pos=None):
        vmin, vmax = self.axis.get_view_interval()
        d = np.rad2deg(abs(vmax - vmin))
        digits = max(-int(np.log10(d) - 1.5), 0)
        # Use unicode rather than mathtext with \circ, so that it will work
        # correctly with any arbitrary font (assuming it has a degree sign),
        # whereas $5\circ$ will only work correctly with one of the supported
        # math fonts (Computer Modern and STIX).
        return ("{value:0.{digits:d}f}\N{DEGREE SIGN}"
                .format(value=np.rad2deg(x), digits=digits))
