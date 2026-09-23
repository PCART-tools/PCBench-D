def _dfi_contains_categorical_data(dfi: Any) -> bool:
    CATEGORICAL_DTYPE = 23
    return any(c.dtype[0] == CATEGORICAL_DTYPE for c in dfi.get_columns())
