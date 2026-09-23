    def get_depth(self, texstr, dpi=120, fontsize=14):
        """
        Returns the offset of the baseline from the bottom of the
        image in pixels.

        *texstr*
            A valid mathtext string, e.g., r'IQ: $\\sigma_i=15$'

        *dpi*
            The dots-per-inch to render the text

        *fontsize*
            The font size in points
        """
        assert(self._output=="bitmap")
        prop = FontProperties(size=fontsize)
        ftimage, depth = self.parse(texstr, dpi=dpi, prop=prop)
        return depth
