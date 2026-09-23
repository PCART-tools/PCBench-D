class YearLocator(DateLocator):
    """
    Make ticks on a given day of each year that is a multiple of base.

    Examples::

      # Tick every year on Jan 1st
      locator = YearLocator()

      # Tick every 5 years on July 4th
      locator = YearLocator(5, month=7, day=4)
    """
    def __init__(self, base=1, month=1, day=1, tz=None):
        """
        Mark years that are multiple of base on a given month and day
        (default jan 1).
        """
        super().__init__(tz)
        self.base = ticker._Edge_integer(base, 0)
        self.replaced = {'month':  month,
                         'day':    day,
                         'hour':   0,
                         'minute': 0,
                         'second': 0,
                         }
        if not hasattr(tz, 'localize'):
            # if tz is pytz, we need to do this w/ the localize fcn,
            # otherwise datetime.replace works fine...
            self.replaced['tzinfo'] = tz

    def __call__(self):
        # if no data have been set, this will tank with a ValueError
        try:
            dmin, dmax = self.viewlim_to_dt()
        except ValueError:
            return []

        return self.tick_values(dmin, dmax)

    def tick_values(self, vmin, vmax):
        ymin = self.base.le(vmin.year) * self.base.step
        ymax = self.base.ge(vmax.year) * self.base.step

        vmin = vmin.replace(year=ymin, **self.replaced)
        if hasattr(self.tz, 'localize'):
            # look after pytz
            if not vmin.tzinfo:
                vmin = self.tz.localize(vmin, is_dst=True)

        ticks = [vmin]

        while True:
            dt = ticks[-1]
            if dt.year >= ymax:
                return date2num(ticks)
            year = dt.year + self.base.step
            dt = dt.replace(year=year, **self.replaced)
            if hasattr(self.tz, 'localize'):
                # look after pytz
                if not dt.tzinfo:
                    dt = self.tz.localize(dt, is_dst=True)

            ticks.append(dt)
