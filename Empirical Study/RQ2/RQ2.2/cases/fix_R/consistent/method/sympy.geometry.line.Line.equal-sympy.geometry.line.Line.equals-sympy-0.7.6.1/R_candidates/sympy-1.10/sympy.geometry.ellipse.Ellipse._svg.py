    def _svg(self, scale_factor=1., fill_color="#66cc99"):
        """Returns SVG ellipse element for the Ellipse.

        Parameters
        ==========

        scale_factor : float
            Multiplication factor for the SVG stroke-width.  Default is 1.
        fill_color : str, optional
            Hex string for fill color. Default is "#66cc99".
        """

        c = N(self.center)
        h, v = N(self.hradius), N(self.vradius)
        return (
            '<ellipse fill="{1}" stroke="#555555" '
            'stroke-width="{0}" opacity="0.6" cx="{2}" cy="{3}" rx="{4}" ry="{5}"/>'
        ).format(2. * scale_factor, fill_color, c.x, c.y, h, v)
