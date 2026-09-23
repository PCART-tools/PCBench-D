    @classmethod
    def from_numpy_dtype(cls, dtype: np.dtype) -> BaseMaskedDtype:
        """
        Construct the MaskedDtype corresponding to the given numpy dtype.
        """
        if dtype.kind == "b":
            from pandas.core.arrays.boolean import BooleanDtype

            return BooleanDtype()
        elif dtype.kind in "iu":
            from pandas.core.arrays.integer import NUMPY_INT_TO_DTYPE

            return NUMPY_INT_TO_DTYPE[dtype]
        elif dtype.kind == "f":
            from pandas.core.arrays.floating import NUMPY_FLOAT_TO_DTYPE

            return NUMPY_FLOAT_TO_DTYPE[dtype]
        else:
            raise NotImplementedError(dtype)
