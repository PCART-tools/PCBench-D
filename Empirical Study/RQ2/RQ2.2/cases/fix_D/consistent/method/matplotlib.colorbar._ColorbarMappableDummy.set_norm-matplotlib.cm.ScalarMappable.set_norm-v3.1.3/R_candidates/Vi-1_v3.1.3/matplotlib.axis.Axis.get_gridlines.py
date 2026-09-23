    def get_gridlines(self):
        'Return the grid lines as a list of Line2D instance'
        ticks = self.get_major_ticks()
        return cbook.silent_list('Line2D gridline',
                                 [tick.gridline for tick in ticks])
