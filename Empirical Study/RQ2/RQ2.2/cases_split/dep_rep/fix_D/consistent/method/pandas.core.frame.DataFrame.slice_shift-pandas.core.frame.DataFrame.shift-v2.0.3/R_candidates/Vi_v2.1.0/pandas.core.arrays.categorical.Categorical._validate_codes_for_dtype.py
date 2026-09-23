    @classmethod
    def _validate_codes_for_dtype(cls, codes, *, dtype: CategoricalDtype) -> np.ndarray:
        if isinstance(codes, ExtensionArray) and is_integer_dtype(codes.dtype):
            # Avoid the implicit conversion of Int to object
            if isna(codes).any():
                raise ValueError("codes cannot contain NA values")
            codes = codes.to_numpy(dtype=np.int64)
        else:
            codes = np.asarray(codes)
        if len(codes) and codes.dtype.kind not in "iu":
            raise ValueError("codes need to be array-like integers")

        if len(codes) and (codes.max() >= len(dtype.categories) or codes.min() < -1):
            raise ValueError("codes need to be between -1 and len(categories)-1")
        return codes
