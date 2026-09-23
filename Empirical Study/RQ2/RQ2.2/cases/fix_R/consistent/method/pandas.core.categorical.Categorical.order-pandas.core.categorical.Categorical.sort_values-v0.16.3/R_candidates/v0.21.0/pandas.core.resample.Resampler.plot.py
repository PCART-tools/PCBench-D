    def plot(self, *args, **kwargs):
        # for compat with prior versions, we want to
        # have the warnings shown here and just have this work
        return self._deprecated('plot').plot(*args, **kwargs)
