    def _parsed_string_to_bounds(self, reso, parsed):
        """
        Calculate datetime bounds for parsed time string and its resolution.

        Parameters
        ----------
        reso : Resolution
            Resolution provided by parsed string.
        parsed : datetime
            Datetime from parsed string.

        Returns
        -------
        lower, upper: pd.Timestamp

        """
        valid_resos = {
            "year",
            "month",
            "quarter",
            "day",
            "hour",
            "minute",
            "second",
            "minute",
            "second",
            "microsecond",
        }
        if reso not in valid_resos:
            raise KeyError
        if reso == "year":
            start = Timestamp(parsed.year, 1, 1)
            end = Timestamp(parsed.year, 12, 31, 23, 59, 59, 999999)
        elif reso == "month":
            d = ccalendar.get_days_in_month(parsed.year, parsed.month)
            start = Timestamp(parsed.year, parsed.month, 1)
            end = Timestamp(parsed.year, parsed.month, d, 23, 59, 59, 999999)
        elif reso == "quarter":
            qe = (((parsed.month - 1) + 2) % 12) + 1  # two months ahead
            d = ccalendar.get_days_in_month(parsed.year, qe)  # at end of month
            start = Timestamp(parsed.year, parsed.month, 1)
            end = Timestamp(parsed.year, qe, d, 23, 59, 59, 999999)
        elif reso == "day":
            start = Timestamp(parsed.year, parsed.month, parsed.day)
            end = start + timedelta(days=1) - Nano(1)
        elif reso == "hour":
            start = Timestamp(parsed.year, parsed.month, parsed.day, parsed.hour)
            end = start + timedelta(hours=1) - Nano(1)
        elif reso == "minute":
            start = Timestamp(
                parsed.year, parsed.month, parsed.day, parsed.hour, parsed.minute
            )
            end = start + timedelta(minutes=1) - Nano(1)
        elif reso == "second":
            start = Timestamp(
                parsed.year,
                parsed.month,
                parsed.day,
                parsed.hour,
                parsed.minute,
                parsed.second,
            )
            end = start + timedelta(seconds=1) - Nano(1)
        elif reso == "microsecond":
            start = Timestamp(
                parsed.year,
                parsed.month,
                parsed.day,
                parsed.hour,
                parsed.minute,
                parsed.second,
                parsed.microsecond,
            )
            end = start + timedelta(microseconds=1) - Nano(1)
        # GH 24076
        # If an incoming date string contained a UTC offset, need to localize
        # the parsed date to this offset first before aligning with the index's
        # timezone
        if parsed.tzinfo is not None:
            if self.tz is None:
                raise ValueError(
                    "The index must be timezone aware "
                    "when indexing with a date string with a "
                    "UTC offset"
                )
            start = start.tz_localize(parsed.tzinfo).tz_convert(self.tz)
            end = end.tz_localize(parsed.tzinfo).tz_convert(self.tz)
        elif self.tz is not None:
            start = start.tz_localize(self.tz)
            end = end.tz_localize(self.tz)
        return start, end
