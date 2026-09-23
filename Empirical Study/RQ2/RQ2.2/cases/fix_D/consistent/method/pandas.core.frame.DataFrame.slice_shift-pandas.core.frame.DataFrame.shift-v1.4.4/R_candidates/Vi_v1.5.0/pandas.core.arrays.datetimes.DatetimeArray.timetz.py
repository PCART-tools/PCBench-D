    @property
    def timetz(self) -> npt.NDArray[np.object_]:
        """
        Returns numpy array of :class:`datetime.time` objects with timezones.

        The time part of the Timestamps.
        """
        return ints_to_pydatetime(self.asi8, self.tz, box="time", reso=self._reso)
