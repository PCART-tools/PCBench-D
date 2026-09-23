    def __setstate__(self, state):
        # Merge the grouping info back into the global groupers.
        shared_axes = state.pop("_shared_axes")
        for name, shared_siblings in shared_axes.items():
            self._shared_axes[name].join(*shared_siblings)
        twinned_siblings = state.pop("_twinned_axes")
        if twinned_siblings:
            self._twinned_axes.join(*twinned_siblings)
        self.__dict__ = state
        self._stale = True
