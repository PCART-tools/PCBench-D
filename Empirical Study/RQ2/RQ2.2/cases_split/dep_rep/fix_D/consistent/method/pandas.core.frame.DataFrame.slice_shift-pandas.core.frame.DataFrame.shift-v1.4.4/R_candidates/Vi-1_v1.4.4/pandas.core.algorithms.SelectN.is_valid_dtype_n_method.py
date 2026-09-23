    @final
    @staticmethod
    def is_valid_dtype_n_method(dtype: DtypeObj) -> bool:
        """
        Helper function to determine if dtype is valid for
        nsmallest/nlargest methods
        """
        return (
            is_numeric_dtype(dtype) and not is_complex_dtype(dtype)
        ) or needs_i8_conversion(dtype)
