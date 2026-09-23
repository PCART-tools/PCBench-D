    def _get_tick_bboxes(self, ticks, renderer):
        """
        Given the list of ticks, return two lists of bboxes. One for
        tick lable1's and another for tick label2's.
        """

        ticklabelBoxes = []
        ticklabelBoxes2 = []

        for tick in ticks:
            if tick.label1On and tick.label1.get_visible():
                extent = tick.label1.get_window_extent(renderer)
                ticklabelBoxes.append(extent)
            if tick.label2On and tick.label2.get_visible():
                extent = tick.label2.get_window_extent(renderer)
                ticklabelBoxes2.append(extent)
        return ticklabelBoxes, ticklabelBoxes2
