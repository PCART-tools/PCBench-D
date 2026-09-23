    def get_values(self, dtype: DtypeObj | None = None) -> np.ndarray:
        """
        return an internal format, currently just the ndarray
        this is often overridden to handle to_dense like operations
        """
        if dtype == _dtype_obj:
            return self.values.astype(_dtype_obj)
        # error: Incompatible return value type (got "Union[ndarray, ExtensionArray]",
        # expected "ndarray")
        return self.values  # type: ignore[return-value]
