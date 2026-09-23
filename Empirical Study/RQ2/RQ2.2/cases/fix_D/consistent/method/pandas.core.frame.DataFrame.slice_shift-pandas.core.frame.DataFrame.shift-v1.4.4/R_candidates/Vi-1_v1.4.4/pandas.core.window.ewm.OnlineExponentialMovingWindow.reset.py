    def reset(self):
        """
        Reset the state captured by `update` calls.
        """
        self._mean.reset()
