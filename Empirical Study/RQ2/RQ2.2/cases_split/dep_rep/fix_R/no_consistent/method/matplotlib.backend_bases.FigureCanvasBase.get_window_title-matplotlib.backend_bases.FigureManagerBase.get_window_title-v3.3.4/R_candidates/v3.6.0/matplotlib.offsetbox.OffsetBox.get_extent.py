    def get_extent(self, renderer):
        """Return a tuple ``width, height, xdescent, ydescent`` of the box."""
        w, h, xd, yd, offsets = self.get_extent_offsets(renderer)
        return w, h, xd, yd
