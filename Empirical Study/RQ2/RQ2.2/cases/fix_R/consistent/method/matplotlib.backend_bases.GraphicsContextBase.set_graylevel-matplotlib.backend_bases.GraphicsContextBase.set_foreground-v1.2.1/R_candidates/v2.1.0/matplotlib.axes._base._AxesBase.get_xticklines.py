    def get_xticklines(self):
        """Get the xtick lines as a list of Line2D instances"""
        return cbook.silent_list('Text xtickline',
                                 self.xaxis.get_ticklines())
