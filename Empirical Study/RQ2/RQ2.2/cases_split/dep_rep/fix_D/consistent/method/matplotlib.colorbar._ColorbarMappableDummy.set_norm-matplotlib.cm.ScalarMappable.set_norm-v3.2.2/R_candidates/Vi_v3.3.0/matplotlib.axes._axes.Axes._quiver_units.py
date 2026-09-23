    def _quiver_units(self, args, kw):
        if len(args) > 3:
            x, y = args[0:2]
            self._process_unit_info(xdata=x, ydata=y, kwargs=kw)
            x = self.convert_xunits(x)
            y = self.convert_yunits(y)
            return (x, y) + args[2:]
        return args
