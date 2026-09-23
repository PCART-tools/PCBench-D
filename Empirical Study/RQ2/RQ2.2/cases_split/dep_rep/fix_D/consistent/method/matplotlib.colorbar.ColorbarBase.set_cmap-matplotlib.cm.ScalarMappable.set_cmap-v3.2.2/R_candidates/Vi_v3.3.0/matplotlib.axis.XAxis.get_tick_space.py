    def get_tick_space(self):
        ends = self.axes.transAxes.transform([[0, 0], [1, 0]])
        length = ((ends[1][0] - ends[0][0]) / self.axes.figure.dpi) * 72
        # There is a heuristic here that the aspect ratio of tick text
        # is no more than 3:1
        size = self._get_tick_label_size('x') * 3
        if size > 0:
            return int(np.floor(length / size))
        else:
            return 2**31 - 1
