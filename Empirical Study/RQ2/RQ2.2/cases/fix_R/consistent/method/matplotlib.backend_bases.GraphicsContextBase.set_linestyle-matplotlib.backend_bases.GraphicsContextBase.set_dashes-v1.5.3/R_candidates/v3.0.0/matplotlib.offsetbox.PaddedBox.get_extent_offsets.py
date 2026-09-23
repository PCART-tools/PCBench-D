    def get_extent_offsets(self, renderer):
        """
        update offset of childrens and return the extents of the box
        """

        dpicor = renderer.points_to_pixels(1.)
        pad = self.pad * dpicor

        w, h, xd, yd = self._children[0].get_extent(renderer)

        return w + 2 * pad, h + 2 * pad, \
               xd + pad, yd + pad, \
               [(0, 0)]
