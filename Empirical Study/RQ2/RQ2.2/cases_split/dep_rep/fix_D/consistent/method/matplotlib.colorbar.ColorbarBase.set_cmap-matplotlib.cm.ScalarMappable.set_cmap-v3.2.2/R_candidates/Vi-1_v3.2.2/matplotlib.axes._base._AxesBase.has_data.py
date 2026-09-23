    def has_data(self):
        """
        Return *True* if any artists have been added to axes.

        This should not be used to determine whether the *dataLim*
        need to be updated, and may not actually be useful for
        anything.
        """
        return (
            len(self.collections) +
            len(self.images) +
            len(self.lines) +
            len(self.patches)) > 0
