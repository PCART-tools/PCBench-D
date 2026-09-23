    def to_mask(self, texstr, dpi=120, fontsize=14):
        """
        *texstr*
            A valid mathtext string, e.g., r'IQ: $\\sigma_i=15$'

        *dpi*
            The dots-per-inch to render the text

        *fontsize*
            The font size in points

        Returns a tuple (*array*, *depth*)

          - *array* is an NxM uint8 alpha ubyte mask array of
            rasterized tex.

          - depth is the offset of the baseline from the bottom of the
            image in pixels.
        """
        assert self._output == "bitmap"
        prop = FontProperties(size=fontsize)
        ftimage, depth = self.parse(texstr, dpi=dpi, prop=prop)

        x = ftimage.as_array()
        return x, depth
