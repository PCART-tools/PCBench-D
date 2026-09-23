    def get_xticklines(self):
        """Get the x tick lines as a list of `Line2D` instances."""
        return cbook.silent_list('Line2D xtickline',
                                 self.xaxis.get_ticklines())
