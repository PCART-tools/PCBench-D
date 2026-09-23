    def get_status(self):
        """
        returns a tuple of the status (True/False) of all of the check buttons
        """
        return [l1.get_visible() for (l1, l2) in self.lines]
