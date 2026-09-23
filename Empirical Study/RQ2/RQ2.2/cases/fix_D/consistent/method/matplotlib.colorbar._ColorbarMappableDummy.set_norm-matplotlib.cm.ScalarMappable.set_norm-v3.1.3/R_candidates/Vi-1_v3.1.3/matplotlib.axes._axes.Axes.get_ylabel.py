    def get_ylabel(self):
        """
        Get the ylabel text string.
        """
        label = self.yaxis.get_label()
        return label.get_text()
