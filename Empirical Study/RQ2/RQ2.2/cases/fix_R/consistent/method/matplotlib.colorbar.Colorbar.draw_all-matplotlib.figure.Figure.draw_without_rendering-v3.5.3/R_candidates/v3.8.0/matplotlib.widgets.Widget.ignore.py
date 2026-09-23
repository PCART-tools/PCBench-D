    def ignore(self, event):
        """
        Return whether *event* should be ignored.

        This method should be called at the beginning of any event callback.
        """
        return not self.active
