    def get_ygridlines(self):
        """Get the y grid lines as a list of Line2D instances"""
        return cbook.silent_list('Line2D ygridline',
                                 self.yaxis.get_gridlines())
