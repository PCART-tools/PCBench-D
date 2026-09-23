    @classmethod
    def _parse_dtype_strict(cls, freq):
        if isinstance(freq, str):
            if freq.startswith("period[") or freq.startswith("Period["):
                m = cls._match.search(freq)
                if m is not None:
                    freq = m.group("freq")
            from pandas.tseries.frequencies import to_offset

            freq = to_offset(freq)
            if freq is not None:
                return freq

        raise ValueError("could not construct PeriodDtype")
