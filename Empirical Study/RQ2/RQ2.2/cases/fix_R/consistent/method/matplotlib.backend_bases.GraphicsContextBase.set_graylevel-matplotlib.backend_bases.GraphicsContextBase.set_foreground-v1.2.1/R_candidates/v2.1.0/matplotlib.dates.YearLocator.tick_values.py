    def tick_values(self, vmin, vmax):
        ymin = self.base.le(vmin.year)
        ymax = self.base.ge(vmax.year)

        ticks = [vmin.replace(year=ymin, **self.replaced)]
        while True:
            dt = ticks[-1]
            if dt.year >= ymax:
                return date2num(ticks)
            year = dt.year + self.base.get_base()
            ticks.append(dt.replace(year=year, **self.replaced))
