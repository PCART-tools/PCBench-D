    def get_window_extent(self, *args, **kwargs):
        """
        get the axes bounding box in display space; *args* and
        *kwargs* are empty
        """
        bbox = self.bbox
        x_pad = 0
        if self.axison and self.xaxis.get_visible():
            x_pad = self.xaxis.get_tick_padding()
        y_pad = 0
        if self.axison and self.yaxis.get_visible():
            y_pad = self.yaxis.get_tick_padding()
        return mtransforms.Bbox([[bbox.x0 - x_pad, bbox.y0 - y_pad],
                                 [bbox.x1 + x_pad, bbox.y1 + y_pad]])
