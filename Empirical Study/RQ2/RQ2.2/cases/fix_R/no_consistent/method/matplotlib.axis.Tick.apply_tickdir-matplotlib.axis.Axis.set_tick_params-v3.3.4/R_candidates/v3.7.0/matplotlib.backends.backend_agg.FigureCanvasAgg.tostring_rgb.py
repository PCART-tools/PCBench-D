    def tostring_rgb(self):
        """
        Get the image as RGB `bytes`.

        `draw` must be called at least once before this function will work and
        to update the renderer for any subsequent changes to the Figure.
        """
        return self.renderer.tostring_rgb()
