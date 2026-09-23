    def autoscale(self):
        """
        Set the view limits to include the data range.
        """
        dmin, dmax = self.datalim_to_dt()
        delta = relativedelta(dmax, dmin)

        # We need to cap at the endpoints of valid datetime
        try:
            start = dmin - delta
        except ValueError:
            start = _from_ordinalf(1.0)

        try:
            stop = dmax + delta
        except ValueError:
            # The magic number!
            stop = _from_ordinalf(3652059.9999999)

        self.rule.set(dtstart=start, until=stop)
        dmin, dmax = self.datalim_to_dt()

        vmin = self.rule.before(dmin, True)
        if not vmin:
            vmin = dmin

        vmax = self.rule.after(dmax, True)
        if not vmax:
            vmax = dmax

        vmin = date2num(vmin)
        vmax = date2num(vmax)

        return self.nonsingular(vmin, vmax)
