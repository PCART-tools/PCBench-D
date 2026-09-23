    def _get_engine_target(self) -> np.ndarray:
        """
        Get the ndarray that we can pass to the IndexEngine constructor.
        """
        # error: Incompatible return value type (got "Union[ExtensionArray,
        # ndarray]", expected "ndarray")
        if type(self) is Index and isinstance(self._values, ExtensionArray):
            # TODO(ExtensionIndex): remove special-case, just use self._values
            return self._values.astype(object)
        return self._values  # type: ignore[return-value]
