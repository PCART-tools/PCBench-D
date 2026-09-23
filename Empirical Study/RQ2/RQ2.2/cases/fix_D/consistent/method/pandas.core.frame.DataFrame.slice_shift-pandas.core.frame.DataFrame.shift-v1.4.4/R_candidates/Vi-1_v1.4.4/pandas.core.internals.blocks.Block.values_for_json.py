    def values_for_json(self) -> np.ndarray:
        # Incompatible return value type (got "Union[ndarray[Any, Any],
        # ExtensionArray]", expected "ndarray[Any, Any]")
        return self.values  # type: ignore[return-value]
