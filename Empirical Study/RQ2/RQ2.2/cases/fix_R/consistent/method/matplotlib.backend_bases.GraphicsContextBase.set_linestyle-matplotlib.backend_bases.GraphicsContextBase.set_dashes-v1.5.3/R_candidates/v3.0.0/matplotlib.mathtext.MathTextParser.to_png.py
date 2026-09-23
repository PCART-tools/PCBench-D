    def to_png(self, filename, texstr, color='black', dpi=120, fontsize=14):
        """
        Writes a tex expression to a PNG file.

        Returns the offset of the baseline from the bottom of the
        image in pixels.

        *filename*
            A writable filename or fileobject

        *texstr*
            A valid mathtext string, e.g., r'IQ: $\\sigma_i=15$'

        *color*
            A valid matplotlib color argument

        *dpi*
            The dots-per-inch to render the text

        *fontsize*
            The font size in points

        Returns the offset of the baseline from the bottom of the
        image in pixels.
        """
        rgba, depth = self.to_rgba(texstr, color=color, dpi=dpi, fontsize=fontsize)
        _png.write_png(rgba, filename)
        return depth
