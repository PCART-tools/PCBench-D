    def set_prop_cycle(self, cycler):
        if cycler is None:
            cycler = mpl.rcParams['axes.prop_cycle']
        self._idx = 0
        self._cycler_items = [*cycler]
