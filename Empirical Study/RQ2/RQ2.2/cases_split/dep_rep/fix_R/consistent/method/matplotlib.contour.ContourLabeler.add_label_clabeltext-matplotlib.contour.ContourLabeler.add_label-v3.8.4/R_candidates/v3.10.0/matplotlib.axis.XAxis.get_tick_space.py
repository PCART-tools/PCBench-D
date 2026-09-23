    def get_tick_space(self):
        ends = mtransforms.Bbox.unit().transformed(
            self.axes.transAxes - self.get_figure(root=False).dpi_scale_trans)
        length = ends.width * 72
        # There is a heuristic here that the aspect ratio of tick text
        # is no more than 3:1
        size = self._get_tick_label_size('x') * 3
        if size > 0:
            return int(np.floor(length / size))
        else:
            return 2**31 - 1
