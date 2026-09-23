    def __getstate__(self):
        d = self.__dict__.copy()
        # remove the unpicklable remove method, this will get re-added on load
        # (by the Axes) if the artist lives on an Axes.
        d['stale_callback'] = None
        return d
