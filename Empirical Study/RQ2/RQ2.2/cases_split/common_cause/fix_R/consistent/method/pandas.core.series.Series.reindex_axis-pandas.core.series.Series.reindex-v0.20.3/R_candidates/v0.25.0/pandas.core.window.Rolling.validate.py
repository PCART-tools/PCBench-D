    def validate(self):
        super().validate()

        # we allow rolling on a datetimelike index
        if (self.obj.empty or self.is_datetimelike) and isinstance(
            self.window, (str, ABCDateOffset, timedelta)
        ):

            self._validate_monotonic()
            freq = self._validate_freq()

            # we don't allow center
            if self.center:
                raise NotImplementedError(
                    "center is not implemented "
                    "for datetimelike and offset "
                    "based windows"
                )

            # this will raise ValueError on non-fixed freqs
            self.win_freq = self.window
            self.window = freq.nanos
            self.win_type = "freq"

            # min_periods must be an integer
            if self.min_periods is None:
                self.min_periods = 1

        elif not is_integer(self.window):
            raise ValueError("window must be an integer")
        elif self.window < 0:
            raise ValueError("window must be non-negative")

        if not self.is_datetimelike and self.closed is not None:
            raise ValueError(
                "closed only implemented for datetimelike " "and offset based windows"
            )
