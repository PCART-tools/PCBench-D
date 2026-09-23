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
        if reso == 'year':
            return (Timestamp(datetime(parsed.year, 1, 1), tz=self.tz),
                    Timestamp(datetime(parsed.year, 12, 31, 23,
                                       59, 59, 999999), tz=self.tz))
        elif reso == 'month':
            d = ccalendar.get_days_in_month(parsed.year, parsed.month)
            return (Timestamp(datetime(parsed.year, parsed.month, 1),
                              tz=self.tz),
                    Timestamp(datetime(parsed.year, parsed.month, d, 23,
                                       59, 59, 999999), tz=self.tz))
        elif reso == 'quarter':
            qe = (((parsed.month - 1) + 2) % 12) + 1  # two months ahead
            d = ccalendar.get_days_in_month(parsed.year, qe)  # at end of month
            return (Timestamp(datetime(parsed.year, parsed.month, 1),
                              tz=self.tz),
                    Timestamp(datetime(parsed.year, qe, d, 23, 59,
                                       59, 999999), tz=self.tz))
        elif reso == 'day':
            st = datetime(parsed.year, parsed.month, parsed.day)
            return (Timestamp(st, tz=self.tz),
                    Timestamp(Timestamp(st + offsets.Day(),
                                        tz=self.tz).value - 1))
        elif reso == 'hour':
            st = datetime(parsed.year, parsed.month, parsed.day,
                          hour=parsed.hour)
            return (Timestamp(st, tz=self.tz),
                    Timestamp(Timestamp(st + offsets.Hour(),
                                        tz=self.tz).value - 1))
        elif reso == 'minute':
            st = datetime(parsed.year, parsed.month, parsed.day,
                          hour=parsed.hour, minute=parsed.minute)
            return (Timestamp(st, tz=self.tz),
                    Timestamp(Timestamp(st + offsets.Minute(),
                                        tz=self.tz).value - 1))
        elif reso == 'second':
            st = datetime(parsed.year, parsed.month, parsed.day,
                          hour=parsed.hour, minute=parsed.minute,
                          second=parsed.second)
            return (Timestamp(st, tz=self.tz),
                    Timestamp(Timestamp(st + offsets.Second(),
                                        tz=self.tz).value - 1))
        elif reso == 'microsecond':
            st = datetime(parsed.year, parsed.month, parsed.day,
                          parsed.hour, parsed.minute, parsed.second,
                          parsed.microsecond)
            return (Timestamp(st, tz=self.tz), Timestamp(st, tz=self.tz))
        else:
            raise KeyError
