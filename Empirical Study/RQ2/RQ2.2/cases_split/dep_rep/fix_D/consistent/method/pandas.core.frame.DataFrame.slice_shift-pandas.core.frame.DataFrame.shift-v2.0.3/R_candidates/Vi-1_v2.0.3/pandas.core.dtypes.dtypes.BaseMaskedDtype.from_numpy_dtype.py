    @classmethod
    def from_numpy_dtype(cls, dtype: np.dtype) -> BaseMaskedDtype:
        """
        Construct the MaskedDtype corresponding to the given numpy dtype.
        """
        if dtype.kind == "b":
            from pandas.core.arrays.boolean import BooleanDtype

            return BooleanDtype()
        elif dtype.kind in ["i", "u"]:
            from pandas.core.arrays.integer import INT_STR_TO_DTYPE

            return INT_STR_TO_DTYPE[dtype.name]
        elif dtype.kind == "f":
            from pandas.core.arrays.floating import FLOAT_STR_TO_DTYPE

            return FLOAT_STR_TO_DTYPE[dtype.name]
        else:
            raise NotImplementedError(dtype)
