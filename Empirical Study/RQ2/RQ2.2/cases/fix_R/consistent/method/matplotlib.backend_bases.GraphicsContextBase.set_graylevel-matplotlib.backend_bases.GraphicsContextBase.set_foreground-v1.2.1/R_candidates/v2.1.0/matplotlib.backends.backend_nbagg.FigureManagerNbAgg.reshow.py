    def reshow(self):
        """
        A special method to re-show the figure in the notebook.

        """
        self._shown = False
        self.show()
