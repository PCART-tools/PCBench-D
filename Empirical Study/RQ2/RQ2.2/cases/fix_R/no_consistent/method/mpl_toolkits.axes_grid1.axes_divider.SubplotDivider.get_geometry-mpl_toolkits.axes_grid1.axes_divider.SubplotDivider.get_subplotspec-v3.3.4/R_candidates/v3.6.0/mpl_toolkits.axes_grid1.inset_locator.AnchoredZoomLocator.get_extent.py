    def get_extent(self, renderer):
        bb = self.parent_axes.transData.transform_bbox(self.axes.viewLim)
        fontsize = renderer.points_to_pixels(self.prop.get_size_in_points())
        pad = self.pad * fontsize
        return (abs(bb.width * self.zoom) + 2 * pad,
                abs(bb.height * self.zoom) + 2 * pad,
                pad, pad)
