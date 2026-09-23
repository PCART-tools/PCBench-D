    def set_antialiased(self, b):
        """
        True if object should be drawn with antialiased rendering
        """

        # use 0, 1 to make life easier on extension code trying to read the gc
        if b:
            self._antialiased = 1
        else:
            self._antialiased = 0
