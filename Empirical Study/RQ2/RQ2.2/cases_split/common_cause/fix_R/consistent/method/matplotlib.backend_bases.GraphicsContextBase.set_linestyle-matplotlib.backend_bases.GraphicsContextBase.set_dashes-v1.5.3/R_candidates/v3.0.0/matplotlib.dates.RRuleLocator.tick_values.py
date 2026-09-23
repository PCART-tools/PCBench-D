    def tick_values(self, vmin, vmax):
        delta = relativedelta(vmax, vmin)

        # We need to cap at the endpoints of valid datetime
        try:
            start = vmin - delta
        except (ValueError, OverflowError):
            start = _from_ordinalf(1.0)

        try:
            stop = vmax + delta
        except (ValueError, OverflowError):
            # The magic number!
            stop = _from_ordinalf(3652059.9999999)

        self.rule.set(dtstart=start, until=stop)

        dates = self.rule.between(vmin, vmax, True)
        if len(dates) == 0:
            return date2num([vmin, vmax])
        return self.raise_if_exceeds(date2num(dates))
