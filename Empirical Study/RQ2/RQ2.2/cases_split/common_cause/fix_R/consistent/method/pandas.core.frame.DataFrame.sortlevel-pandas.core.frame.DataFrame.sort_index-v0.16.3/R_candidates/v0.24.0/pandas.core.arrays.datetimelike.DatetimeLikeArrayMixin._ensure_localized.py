    def _ensure_localized(self, arg, ambiguous='raise', nonexistent='raise',
                          from_utc=False):
        """
        Ensure that we are re-localized.

        This is for compat as we can then call this on all datetimelike
        arrays generally (ignored for Period/Timedelta)

        Parameters
        ----------
        arg : Union[DatetimeLikeArray, DatetimeIndexOpsMixin, ndarray]
        ambiguous : str, bool, or bool-ndarray, default 'raise'
        nonexistent : str, default 'raise'
        from_utc : bool, default False
            If True, localize the i8 ndarray to UTC first before converting to
            the appropriate tz. If False, localize directly to the tz.

        Returns
        -------
        localized array
        """

        # reconvert to local tz
        tz = getattr(self, 'tz', None)
        if tz is not None:
            if not isinstance(arg, type(self)):
                arg = self._simple_new(arg)
            if from_utc:
                arg = arg.tz_localize('UTC').tz_convert(self.tz)
            else:
                arg = arg.tz_localize(
                    self.tz, ambiguous=ambiguous, nonexistent=nonexistent
                )
        return arg
