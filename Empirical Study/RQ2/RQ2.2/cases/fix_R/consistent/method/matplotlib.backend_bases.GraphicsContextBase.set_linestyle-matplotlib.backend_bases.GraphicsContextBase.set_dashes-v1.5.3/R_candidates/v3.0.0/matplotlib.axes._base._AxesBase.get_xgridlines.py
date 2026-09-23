    def get_xgridlines(self):
        """Get the x grid lines as a list of `Line2D` instances."""
        return cbook.silent_list('Line2D xgridline',
                                 self.xaxis.get_gridlines())
