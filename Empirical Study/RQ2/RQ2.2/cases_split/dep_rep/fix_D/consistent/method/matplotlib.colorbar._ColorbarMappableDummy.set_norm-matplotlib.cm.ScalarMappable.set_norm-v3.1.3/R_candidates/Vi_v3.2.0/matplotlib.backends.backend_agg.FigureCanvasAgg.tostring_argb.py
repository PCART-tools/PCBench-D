    def tostring_argb(self):
        """Get the image as an ARGB byte string.

        `draw` must be called at least once before this function will work and
        to update the renderer for any subsequent changes to the Figure.

        Returns
        -------
        bytes
        """
        return self.renderer.tostring_argb()
