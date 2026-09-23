    def _quiver_units(self, args, kwargs):
        if len(args) > 3:
            x, y = args[0:2]
            x, y = self._process_unit_info([("x", x), ("y", y)], kwargs)
            return (x, y) + args[2:]
        return args
