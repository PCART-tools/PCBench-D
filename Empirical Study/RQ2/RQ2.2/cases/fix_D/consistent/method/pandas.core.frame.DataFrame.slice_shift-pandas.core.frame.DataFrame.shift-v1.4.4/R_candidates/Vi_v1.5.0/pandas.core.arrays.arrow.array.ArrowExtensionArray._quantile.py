    def _quantile(
        self: ArrowExtensionArrayT, qs: npt.NDArray[np.float64], interpolation: str
    ) -> ArrowExtensionArrayT:
        """
        Compute the quantiles of self for each quantile in `qs`.

        Parameters
        ----------
        qs : np.ndarray[float64]
        interpolation: str

        Returns
        -------
        same type as self
        """
        if pa_version_under4p0:
            raise NotImplementedError(
                "quantile only supported for pyarrow version >= 4.0"
            )
        result = pc.quantile(self._data, q=qs, interpolation=interpolation)
        return type(self)(result)
