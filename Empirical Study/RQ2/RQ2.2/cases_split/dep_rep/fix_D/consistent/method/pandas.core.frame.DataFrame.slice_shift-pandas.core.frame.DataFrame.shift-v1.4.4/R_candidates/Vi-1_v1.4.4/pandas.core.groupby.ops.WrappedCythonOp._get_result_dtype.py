    def _get_result_dtype(self, dtype: DtypeObj) -> DtypeObj:
        """
        Get the desired dtype of a result based on the
        input dtype and how it was computed.

        Parameters
        ----------
        dtype : np.dtype or ExtensionDtype
            Input dtype.

        Returns
        -------
        np.dtype or ExtensionDtype
            The desired dtype of the result.
        """
        how = self.how

        if how in ["add", "cumsum", "sum", "prod"]:
            if dtype == np.dtype(bool):
                return np.dtype(np.int64)
            elif isinstance(dtype, (BooleanDtype, _IntegerDtype)):
                return Int64Dtype()
        elif how in ["mean", "median", "var"]:
            if isinstance(dtype, (BooleanDtype, _IntegerDtype)):
                return Float64Dtype()
            elif is_float_dtype(dtype) or is_complex_dtype(dtype):
                return dtype
            elif is_numeric_dtype(dtype):
                return np.dtype(np.float64)
        return dtype
