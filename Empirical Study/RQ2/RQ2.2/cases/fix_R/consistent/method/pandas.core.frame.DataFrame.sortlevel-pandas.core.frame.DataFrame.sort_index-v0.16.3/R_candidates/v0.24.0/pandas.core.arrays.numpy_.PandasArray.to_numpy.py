    def to_numpy(self, dtype=None, copy=False):
        """
        Convert the PandasArray to a :class:`numpy.ndarray`.

        By default, this requires no coercion or copying of data.

        Parameters
        ----------
        dtype : numpy.dtype
            The NumPy dtype to pass to :func:`numpy.asarray`.
        copy : bool, default False
            Whether to copy the underlying data.

        Returns
        -------
        ndarray
        """
        result = np.asarray(self._ndarray, dtype=dtype)
        if copy and result is self._ndarray:
            result = result.copy()

        return result
