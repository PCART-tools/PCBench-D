    def reset(self) -> None:
        """
        Reset the state captured by `update` calls.
        """
        self._mean.reset()
