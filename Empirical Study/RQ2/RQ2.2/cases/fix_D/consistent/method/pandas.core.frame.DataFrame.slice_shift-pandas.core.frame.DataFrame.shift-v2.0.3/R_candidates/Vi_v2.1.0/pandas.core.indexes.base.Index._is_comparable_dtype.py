    def _is_comparable_dtype(self, dtype: DtypeObj) -> bool:
        """
        Can we compare values of the given dtype to our own?
        """
        if self.dtype.kind == "b":
            return dtype.kind == "b"
        elif is_numeric_dtype(self.dtype):
            return is_numeric_dtype(dtype)
        # TODO: this was written assuming we only get here with object-dtype,
        #  which is no longer correct. Can we specialize for EA?
        return True
