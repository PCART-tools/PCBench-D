    def to_rgba(self, texstr, color='black', dpi=120, fontsize=14):
        """
        *texstr*
            A valid mathtext string, e.g., r'IQ: $\\sigma_i=15$'

        *color*
            Any matplotlib color argument

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
        x, depth = self.to_mask(texstr, dpi=dpi, fontsize=fontsize)

        r, g, b, a = mcolors.to_rgba(color)
        RGBA = np.zeros((x.shape[0], x.shape[1], 4), dtype=np.uint8)
        RGBA[:, :, 0] = 255 * r
        RGBA[:, :, 1] = 255 * g
        RGBA[:, :, 2] = 255 * b
        RGBA[:, :, 3] = x
        return RGBA, depth
