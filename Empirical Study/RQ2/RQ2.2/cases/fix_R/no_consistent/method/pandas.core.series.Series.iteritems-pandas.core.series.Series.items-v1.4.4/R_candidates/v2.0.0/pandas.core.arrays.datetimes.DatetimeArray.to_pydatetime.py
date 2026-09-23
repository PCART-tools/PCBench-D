    def to_pydatetime(self) -> npt.NDArray[np.object_]:
        """
        Return an ndarray of datetime.datetime objects.

        Returns
        -------
        numpy.ndarray
        """
        return ints_to_pydatetime(self.asi8, tz=self.tz, reso=self._creso)
