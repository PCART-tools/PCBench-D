    def autoscale(self):
        """
        Set the view limits to include the data range.
        """
        dmin, dmax = self.datalim_to_dt()

        ymin = self.base.le(dmin.year)
        ymax = self.base.ge(dmax.year)
        vmin = dmin.replace(year=ymin, **self.replaced)
        vmax = dmax.replace(year=ymax, **self.replaced)

        vmin = date2num(vmin)
        vmax = date2num(vmax)
        return self.nonsingular(vmin, vmax)
