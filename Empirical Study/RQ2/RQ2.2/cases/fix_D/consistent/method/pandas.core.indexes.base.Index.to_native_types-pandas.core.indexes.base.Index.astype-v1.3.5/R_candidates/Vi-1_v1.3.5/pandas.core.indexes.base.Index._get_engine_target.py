    def _get_engine_target(self) -> np.ndarray:
        """
        Get the ndarray that we can pass to the IndexEngine constructor.
        """
        # error: Incompatible return value type (got "Union[ExtensionArray,
        # ndarray]", expected "ndarray")
        return self._values  # type: ignore[return-value]
