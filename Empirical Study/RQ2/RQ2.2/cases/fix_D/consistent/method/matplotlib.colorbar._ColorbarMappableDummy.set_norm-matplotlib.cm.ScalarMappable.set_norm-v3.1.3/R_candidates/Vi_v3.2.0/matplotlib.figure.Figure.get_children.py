    def get_children(self):
        """Get a list of artists contained in the figure."""
        return [self.patch,
                *self.artists,
                *self.axes,
                *self.lines,
                *self.patches,
                *self.texts,
                *self.images,
                *self.legends]
