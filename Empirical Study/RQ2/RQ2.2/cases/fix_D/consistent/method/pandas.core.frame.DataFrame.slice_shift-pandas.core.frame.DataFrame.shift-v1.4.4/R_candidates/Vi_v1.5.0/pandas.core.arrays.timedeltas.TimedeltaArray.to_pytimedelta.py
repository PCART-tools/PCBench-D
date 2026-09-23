    def to_pytimedelta(self) -> npt.NDArray[np.object_]:
        """
        Return an ndarray of datetime.timedelta objects.

        Returns
        -------
        timedeltas : ndarray[object]
        """
        return ints_to_pytimedelta(self._ndarray)
