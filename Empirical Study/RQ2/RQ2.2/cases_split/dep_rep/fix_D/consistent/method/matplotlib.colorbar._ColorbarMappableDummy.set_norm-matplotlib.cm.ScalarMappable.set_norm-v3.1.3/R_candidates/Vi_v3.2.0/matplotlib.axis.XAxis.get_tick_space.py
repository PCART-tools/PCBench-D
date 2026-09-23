    def get_tick_space(self):
        ends = self.axes.transAxes.transform([[0, 0], [1, 0]])
        length = ((ends[1][0] - ends[0][0]) / self.axes.figure.dpi) * 72
        tick = self._get_tick(True)
        # There is a heuristic here that the aspect ratio of tick text
        # is no more than 3:1
        size = tick.label1.get_size() * 3
        if size > 0:
            return int(np.floor(length / size))
        else:
            return 2**31 - 1
