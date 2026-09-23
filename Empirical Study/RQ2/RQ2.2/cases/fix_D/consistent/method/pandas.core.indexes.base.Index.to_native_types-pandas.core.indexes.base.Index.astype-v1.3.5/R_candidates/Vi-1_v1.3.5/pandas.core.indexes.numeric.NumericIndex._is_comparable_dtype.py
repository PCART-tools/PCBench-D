    def _is_comparable_dtype(self, dtype: DtypeObj) -> bool:
        # If we ever have BoolIndex or ComplexIndex, this may need to be tightened
        return is_numeric_dtype(dtype)
