    def to_mask(self, texstr, dpi=120, fontsize=14):
        r"""
        Parameters
        ----------
        texstr : str
            A valid mathtext string, e.g., r'IQ: $\sigma_i=15$'.
        dpi : float
            The dots-per-inch setting used to render the text.
        fontsize : int
            The font size in points

        Returns
        -------
        array : 2D uint8 alpha
            Mask array of rasterized tex.
        depth : int
            Offset of the baseline from the bottom of the image, in pixels.
        """
        assert self._output == "bitmap"
        prop = FontProperties(size=fontsize)
        ftimage, depth = self.parse(texstr, dpi=dpi, prop=prop)
        return np.asarray(ftimage), depth
