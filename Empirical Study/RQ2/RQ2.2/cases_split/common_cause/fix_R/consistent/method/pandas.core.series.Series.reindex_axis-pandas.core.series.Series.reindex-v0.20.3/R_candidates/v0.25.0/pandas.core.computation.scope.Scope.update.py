    def update(self, level):
        """Update the current scope by going back `level` levels.

        Parameters
        ----------
        level : int or None, optional, default None
        """
        sl = level + 1

        # add sl frames to the scope starting with the
        # most distant and overwriting with more current
        # makes sure that we can capture variable scope
        stack = inspect.stack()

        try:
            self._get_vars(stack[:sl], scopes=["locals"])
        finally:
            del stack[:], stack
