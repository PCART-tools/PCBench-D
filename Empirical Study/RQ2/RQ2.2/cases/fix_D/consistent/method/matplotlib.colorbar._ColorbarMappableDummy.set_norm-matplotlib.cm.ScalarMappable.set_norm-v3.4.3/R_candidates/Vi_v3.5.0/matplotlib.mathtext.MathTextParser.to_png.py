    @_api.deprecated("3.4", alternative="mathtext.math_to_image")
    def to_png(self, filename, texstr, color='black', dpi=120, fontsize=14):
        r"""
        Render a tex expression to a PNG file.

        Parameters
        ----------
        filename
            A writable filename or fileobject.
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
        int
            Offset of the baseline from the bottom of the image, in pixels.
        """
        rgba, depth = self.to_rgba(
            texstr, color=color, dpi=dpi, fontsize=fontsize)
        Image.fromarray(rgba).save(filename, format="png")
        return depth
