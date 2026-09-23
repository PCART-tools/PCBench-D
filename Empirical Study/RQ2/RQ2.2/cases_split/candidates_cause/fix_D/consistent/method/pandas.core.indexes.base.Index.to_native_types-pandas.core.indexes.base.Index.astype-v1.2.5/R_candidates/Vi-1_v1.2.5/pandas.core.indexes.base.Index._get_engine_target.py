    def _get_engine_target(self) -> np.ndarray:
        """
        Get the ndarray that we can pass to the IndexEngine constructor.
        """
        return self._values
