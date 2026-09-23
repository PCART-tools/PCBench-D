    def get_yticklines(self):
        """Get the y tick lines as a list of `Line2D` instances."""
        return cbook.silent_list('Line2D ytickline',
                                 self.yaxis.get_ticklines())
