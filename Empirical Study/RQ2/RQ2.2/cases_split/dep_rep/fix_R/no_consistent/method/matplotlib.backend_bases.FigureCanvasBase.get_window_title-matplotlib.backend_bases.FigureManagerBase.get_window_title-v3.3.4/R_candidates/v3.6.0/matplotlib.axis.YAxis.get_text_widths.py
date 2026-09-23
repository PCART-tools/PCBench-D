    @_api.deprecated("3.6")
    def get_text_widths(self, renderer):
        bbox, bbox2 = self.get_ticklabel_extents(renderer)
        # MGDTODO: Need a better way to get the pad
        pad_pixels = self.majorTicks[0].get_pad_pixels()

        left = 0.0
        if bbox.width:
            left += bbox.width + pad_pixels
        right = 0.0
        if bbox2.width:
            right += bbox2.width + pad_pixels

        if self.get_label_position() == 'left':
            left += self.label.get_window_extent(renderer).width + pad_pixels
        else:
            right += self.label.get_window_extent(renderer).width + pad_pixels
        return left, right
