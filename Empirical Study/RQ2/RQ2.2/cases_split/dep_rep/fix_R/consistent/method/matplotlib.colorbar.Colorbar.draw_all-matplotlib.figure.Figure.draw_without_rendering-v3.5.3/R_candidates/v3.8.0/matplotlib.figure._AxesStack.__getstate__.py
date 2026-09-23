    def __getstate__(self):
        return {
            **vars(self),
            "_counter": max(self._axes.values(), default=0)
        }
