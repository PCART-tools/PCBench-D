    def get_lines(self):
        """Return a list of lines contained by the Axes"""
        return cbook.silent_list('Line2D', self.lines)
