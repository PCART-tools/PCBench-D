    def _get_join_target(self) -> np.ndarray:
        """
        Get the ndarray that we will pass to libjoin functions.
        """
        return self._get_engine_target()
