    def get_text_widths(self, renderer):
        bbox, bbox2 = self.get_ticklabel_extents(renderer)
        # MGDTODO: Need a better way to get the pad
        padPixels = self.majorTicks[0].get_pad_pixels()

        left = 0.0
        if bbox.width:
            left += bbox.width + padPixels
        right = 0.0
        if bbox2.width:
            right += bbox2.width + padPixels

        if self.get_label_position() == 'left':
            left += self.label.get_window_extent(renderer).width + padPixels
        else:
            right += self.label.get_window_extent(renderer).width + padPixels
        return left, right
