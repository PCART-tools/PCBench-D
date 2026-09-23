    def _create_rrule(self, vmin, vmax):
        # 'start' needs to be a multiple of the interval to create ticks on
        # interval multiples when the tick frequency is YEARLY
        ymin = max(self.base.le(vmin.year) * self.base.step, 1)
        ymax = min(self.base.ge(vmax.year) * self.base.step, 9999)

        c = self.rule._construct
        replace = {'year': ymin,
                   'month': c.get('bymonth', 1),
                   'day': c.get('bymonthday', 1),
                   'hour': 0, 'minute': 0, 'second': 0}

        start = vmin.replace(**replace)
        stop = start.replace(year=ymax)
        self.rule.set(dtstart=start, until=stop)

        return start, stop
