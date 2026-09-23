    def _format_native_types(
        self, *, na_rep="NaT", date_format=None
    ) -> npt.NDArray[np.object_]:
        """
        Helper method for astype when converting to strings.

        Returns
        -------
        ndarray[str]
        """
        raise AbstractMethodError(self)
