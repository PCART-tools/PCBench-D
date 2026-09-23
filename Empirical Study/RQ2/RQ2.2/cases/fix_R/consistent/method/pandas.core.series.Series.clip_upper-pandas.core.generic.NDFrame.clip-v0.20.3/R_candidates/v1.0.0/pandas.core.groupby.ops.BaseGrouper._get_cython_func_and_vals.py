    def _get_cython_func_and_vals(
        self, kind: str, how: str, values: np.ndarray, is_numeric: bool
    ):
        """
        Find the appropriate cython function, casting if necessary.

        Parameters
        ----------
        kind : sttr
        how : srt
        values : np.ndarray
        is_numeric : bool

        Returns
        -------
        func : callable
        values : np.ndarray
        """
        try:
            func = self._get_cython_function(kind, how, values, is_numeric)
        except NotImplementedError:
            if is_numeric:
                try:
                    values = ensure_float64(values)
                except TypeError:
                    if lib.infer_dtype(values, skipna=False) == "complex":
                        values = values.astype(complex)
                    else:
                        raise
                func = self._get_cython_function(kind, how, values, is_numeric)
            else:
                raise
        return func, values
