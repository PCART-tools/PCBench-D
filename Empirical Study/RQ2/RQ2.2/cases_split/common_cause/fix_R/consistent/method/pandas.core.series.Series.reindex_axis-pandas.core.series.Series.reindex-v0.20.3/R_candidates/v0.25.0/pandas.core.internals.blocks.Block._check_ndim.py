    def _check_ndim(self, values, ndim):
        """
        ndim inference and validation.

        Infers ndim from 'values' if not provided to __init__.
        Validates that values.ndim and ndim are consistent if and only if
        the class variable '_validate_ndim' is True.

        Parameters
        ----------
        values : array-like
        ndim : int or None

        Returns
        -------
        ndim : int

        Raises
        ------
        ValueError : the number of dimensions do not match
        """
        if ndim is None:
            ndim = values.ndim

        if self._validate_ndim and values.ndim != ndim:
            msg = "Wrong number of dimensions. values.ndim != ndim [{} != {}]"
            raise ValueError(msg.format(values.ndim, ndim))

        return ndim
