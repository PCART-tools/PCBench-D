    @_api.deprecated("3.4", alternative="mathtext.math_to_image")
    def to_rgba(self, texstr, color='black', dpi=120, fontsize=14):
        r"""
        Convert a mathtext string to an RGBA array and depth.

        Parameters
        ----------
        texstr : str
            A valid mathtext string, e.g., r'IQ: $\sigma_i=15$'.
        color : color
            The text color.
        dpi : float
            The dots-per-inch setting used to render the text.
        fontsize : int
            The font size in points.

        Returns
        -------
        array : (M, N, 4) array
            RGBA color values of rasterized tex, colorized with *color*.
        depth : int
            Offset of the baseline from the bottom of the image, in pixels.
        """
        x, depth = self.to_mask(texstr, dpi=dpi, fontsize=fontsize)

        r, g, b, a = mcolors.to_rgba(color)
        RGBA = np.zeros((x.shape[0], x.shape[1], 4), dtype=np.uint8)
        RGBA[:, :, 0] = 255 * r
        RGBA[:, :, 1] = 255 * g
        RGBA[:, :, 2] = 255 * b
        RGBA[:, :, 3] = x
        return RGBA, depth
