    def _parsed_string_to_bounds(self, reso, parsed):
        if reso == "year":
            t1 = Period(year=parsed.year, freq="A")
        elif reso == "month":
            t1 = Period(year=parsed.year, month=parsed.month, freq="M")
        elif reso == "quarter":
            q = (parsed.month - 1) // 3 + 1
            t1 = Period(year=parsed.year, quarter=q, freq="Q-DEC")
        elif reso == "day":
            t1 = Period(year=parsed.year, month=parsed.month, day=parsed.day, freq="D")
        elif reso == "hour":
            t1 = Period(
                year=parsed.year,
                month=parsed.month,
                day=parsed.day,
                hour=parsed.hour,
                freq="H",
            )
        elif reso == "minute":
            t1 = Period(
                year=parsed.year,
                month=parsed.month,
                day=parsed.day,
                hour=parsed.hour,
                minute=parsed.minute,
                freq="T",
            )
        elif reso == "second":
            t1 = Period(
                year=parsed.year,
                month=parsed.month,
                day=parsed.day,
                hour=parsed.hour,
                minute=parsed.minute,
                second=parsed.second,
                freq="S",
            )
        else:
            raise KeyError(reso)
        return (t1.asfreq(self.freq, how="start"), t1.asfreq(self.freq, how="end"))
