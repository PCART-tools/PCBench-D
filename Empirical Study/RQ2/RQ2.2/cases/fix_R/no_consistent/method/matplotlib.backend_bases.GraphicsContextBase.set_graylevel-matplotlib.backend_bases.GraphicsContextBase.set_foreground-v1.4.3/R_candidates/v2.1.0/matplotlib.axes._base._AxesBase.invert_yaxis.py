    def invert_yaxis(self):
        """
        Invert the y-axis.
        """
        bottom, top = self.get_ylim()
        self.set_ylim(top, bottom, auto=None)
