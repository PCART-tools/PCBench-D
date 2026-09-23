    def get_lines(self):
        'Return a list of `~.lines.Line2D` instances in the legend.'
        return [h for h in self.legendHandles if isinstance(h, Line2D)]
