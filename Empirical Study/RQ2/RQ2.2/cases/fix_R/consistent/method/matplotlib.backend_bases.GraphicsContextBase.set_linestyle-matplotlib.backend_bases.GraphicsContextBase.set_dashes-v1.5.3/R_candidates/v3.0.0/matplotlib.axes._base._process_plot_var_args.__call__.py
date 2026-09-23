    def __call__(self, *args, **kwargs):
        if self.axes.xaxis is not None and self.axes.yaxis is not None:
            xunits = kwargs.pop('xunits', self.axes.xaxis.units)

            if self.axes.name == 'polar':
                xunits = kwargs.pop('thetaunits', xunits)

            yunits = kwargs.pop('yunits', self.axes.yaxis.units)

            if self.axes.name == 'polar':
                yunits = kwargs.pop('runits', yunits)

            if xunits != self.axes.xaxis.units:
                self.axes.xaxis.set_units(xunits)

            if yunits != self.axes.yaxis.units:
                self.axes.yaxis.set_units(yunits)

        ret = self._grab_next_args(*args, **kwargs)
        return ret
