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
