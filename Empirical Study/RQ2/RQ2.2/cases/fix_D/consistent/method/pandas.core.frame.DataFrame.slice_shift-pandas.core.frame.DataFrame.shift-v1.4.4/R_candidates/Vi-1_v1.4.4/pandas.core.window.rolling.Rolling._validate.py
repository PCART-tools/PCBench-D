    def _validate(self):
        super()._validate()

        # we allow rolling on a datetimelike index
        if (
            self.obj.empty
            or isinstance(self._on, (DatetimeIndex, TimedeltaIndex, PeriodIndex))
        ) and isinstance(self.window, (str, BaseOffset, timedelta)):

            self._validate_datetimelike_monotonic()

            # this will raise ValueError on non-fixed freqs
            try:
                freq = to_offset(self.window)
            except (TypeError, ValueError) as err:
                raise ValueError(
                    f"passed window {self.window} is not "
                    "compatible with a datetimelike index"
                ) from err
            if isinstance(self._on, PeriodIndex):
                self._win_freq_i8 = freq.nanos / (self._on.freq.nanos / self._on.freq.n)
            else:
                self._win_freq_i8 = freq.nanos

            # min_periods must be an integer
            if self.min_periods is None:
                self.min_periods = 1

        elif isinstance(self.window, BaseIndexer):
            # Passed BaseIndexer subclass should handle all other rolling kwargs
            return
        elif not is_integer(self.window) or self.window < 0:
            raise ValueError("window must be an integer 0 or greater")
