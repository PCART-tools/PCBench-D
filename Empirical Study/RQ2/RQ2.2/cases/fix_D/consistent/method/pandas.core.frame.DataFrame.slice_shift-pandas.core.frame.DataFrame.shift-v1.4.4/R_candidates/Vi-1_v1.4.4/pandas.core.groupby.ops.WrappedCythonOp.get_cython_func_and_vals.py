    def get_cython_func_and_vals(self, values: np.ndarray, is_numeric: bool):
        """
        Find the appropriate cython function, casting if necessary.

        Parameters
        ----------
        values : np.ndarray
        is_numeric : bool

        Returns
        -------
        func : callable
        values : np.ndarray
        """
        how = self.how
        kind = self.kind

        if how in ["median", "cumprod"]:
            # these two only have float64 implementations
            if is_numeric:
                values = ensure_float64(values)
            else:
                raise NotImplementedError(
                    f"function is not implemented for this dtype: "
                    f"[how->{how},dtype->{values.dtype.name}]"
                )
            func = getattr(libgroupby, f"group_{how}_float64")
            return func, values

        func = self._get_cython_function(kind, how, values.dtype, is_numeric)

        if values.dtype.kind in ["i", "u"]:
            if how in ["add", "var", "prod", "mean", "ohlc"]:
                # result may still include NaN, so we have to cast
                values = ensure_float64(values)

        return func, values
