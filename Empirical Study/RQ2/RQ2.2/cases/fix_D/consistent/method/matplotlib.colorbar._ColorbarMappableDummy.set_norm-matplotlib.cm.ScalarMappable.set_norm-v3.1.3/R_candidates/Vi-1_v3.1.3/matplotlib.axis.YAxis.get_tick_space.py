    def get_tick_space(self):
        ends = self.axes.transAxes.transform([[0, 0], [0, 1]])
        length = ((ends[1][1] - ends[0][1]) / self.axes.figure.dpi) * 72
        tick = self._get_tick(True)
        # Having a spacing of at least 2 just looks good.
        size = tick.label1.get_size() * 2.0
        if size > 0:
            return int(np.floor(length / size))
        else:
            return 2**31 - 1
