    def get_gridlines(self):
        r"""Return this Axis' grid lines as a list of `.Line2D`\s."""
        ticks = self.get_major_ticks()
        return cbook.silent_list('Line2D gridline',
                                 [tick.gridline for tick in ticks])
