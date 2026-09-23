    def set_prop_cycle(self, *args, **kwargs):
        if not (args or kwargs) or (len(args) == 1 and args[0] is None):
            prop_cycler = rcParams['axes.prop_cycle']
        else:
            prop_cycler = cycler(*args, **kwargs)

        self.prop_cycler = itertools.cycle(prop_cycler)
        # This should make a copy
        self._prop_keys = prop_cycler.keys
