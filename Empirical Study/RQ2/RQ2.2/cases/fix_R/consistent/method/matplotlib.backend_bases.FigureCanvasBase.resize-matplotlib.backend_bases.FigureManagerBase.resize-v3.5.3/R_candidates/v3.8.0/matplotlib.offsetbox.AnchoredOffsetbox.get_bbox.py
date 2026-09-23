    def get_bbox(self, renderer):
        # docstring inherited
        fontsize = renderer.points_to_pixels(self.prop.get_size_in_points())
        pad = self.pad * fontsize
        return self.get_child().get_bbox(renderer).padded(pad)
