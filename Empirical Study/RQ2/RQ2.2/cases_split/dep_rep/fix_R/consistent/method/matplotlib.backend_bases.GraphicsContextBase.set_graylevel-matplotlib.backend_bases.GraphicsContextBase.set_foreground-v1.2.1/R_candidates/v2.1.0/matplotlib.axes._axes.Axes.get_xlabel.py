    def get_xlabel(self):
        """
        Get the xlabel text string.
        """
        label = self.xaxis.get_label()
        return label.get_text()
