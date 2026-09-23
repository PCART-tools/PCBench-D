    def __call__(self, x, pos=None):
        vmin, vmax = self.axis.get_view_interval()
        d = np.rad2deg(abs(vmax - vmin))
        digits = max(-int(np.log10(d) - 1.5), 0)

        if rcParams['text.usetex'] and not rcParams['text.latex.unicode']:
            format_str = r"${value:0.{digits:d}f}^\circ$"
            return format_str.format(value=np.rad2deg(x), digits=digits)
        else:
            # we use unicode, rather than mathtext with \circ, so
            # that it will work correctly with any arbitrary font
            # (assuming it has a degree sign), whereas $5\circ$
            # will only work correctly with one of the supported
            # math fonts (Computer Modern and STIX)
            format_str = "{value:0.{digits:d}f}\N{DEGREE SIGN}"
            return format_str.format(value=np.rad2deg(x), digits=digits)
