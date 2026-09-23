    def tick_values(self, vmin, vmax):
        start, stop = self._create_rrule(vmin, vmax)
        dates = self.rule.between(start, stop, True)
        if len(dates) == 0:
            return date2num([vmin, vmax])
        return self.raise_if_exceeds(date2num(dates))
