    def _svg(self, scale_factor=1., fill_color="#66cc99"):
        """Returns SVG path element for the LinearEntity.

        Parameters
        ==========

        scale_factor : float
            Multiplication factor for the SVG stroke-width.  Default is 1.
        fill_color : str, optional
            Hex string for fill color. Default is "#66cc99".
        """
        verts = (N(self.p1), N(self.p2))
        coords = ["{},{}".format(p.x, p.y) for p in verts]
        path = "M {} L {}".format(coords[0], " L ".join(coords[1:]))
        return (
            '<path fill-rule="evenodd" fill="{2}" stroke="#555555" '
            'stroke-width="{0}" opacity="0.6" d="{1}" />'
        ).format(2.*scale_factor, path, fill_color)
