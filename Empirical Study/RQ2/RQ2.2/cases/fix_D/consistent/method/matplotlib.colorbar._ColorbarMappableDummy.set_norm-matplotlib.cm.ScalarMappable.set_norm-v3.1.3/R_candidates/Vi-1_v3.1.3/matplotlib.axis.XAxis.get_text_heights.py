    def get_text_heights(self, renderer):
        """
        Returns the amount of space one should reserve for text
        above and below the axes.  Returns a tuple (above, below)
        """
        bbox, bbox2 = self.get_ticklabel_extents(renderer)
        # MGDTODO: Need a better way to get the pad
        padPixels = self.majorTicks[0].get_pad_pixels()

        above = 0.0
        if bbox2.height:
            above += bbox2.height + padPixels
        below = 0.0
        if bbox.height:
            below += bbox.height + padPixels

        if self.get_label_position() == 'top':
            above += self.label.get_window_extent(renderer).height + padPixels
        else:
            below += self.label.get_window_extent(renderer).height + padPixels
        return above, below
