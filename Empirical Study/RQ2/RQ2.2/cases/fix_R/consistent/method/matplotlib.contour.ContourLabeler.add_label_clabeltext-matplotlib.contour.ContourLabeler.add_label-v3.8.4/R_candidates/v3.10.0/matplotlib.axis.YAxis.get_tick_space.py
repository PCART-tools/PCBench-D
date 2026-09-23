    def get_tick_space(self):
        ends = mtransforms.Bbox.unit().transformed(
            self.axes.transAxes - self.get_figure(root=False).dpi_scale_trans)
        length = ends.height * 72
        # Having a spacing of at least 2 just looks good.
        size = self._get_tick_label_size('y') * 2
        if size > 0:
            return int(np.floor(length / size))
        else:
            return 2**31 - 1
