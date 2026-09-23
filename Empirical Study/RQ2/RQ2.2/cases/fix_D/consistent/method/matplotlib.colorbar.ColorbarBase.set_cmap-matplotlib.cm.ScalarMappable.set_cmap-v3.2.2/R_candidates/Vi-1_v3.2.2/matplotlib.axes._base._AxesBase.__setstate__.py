    def __setstate__(self, state):
        # Merge the grouping info back into the global groupers.
        for grouper_name in [
                '_shared_x_axes', '_shared_y_axes', '_twinned_axes']:
            siblings = state.pop(grouper_name)
            if siblings:
                getattr(self, grouper_name).join(*siblings)
        self.__dict__ = state
        self._stale = True
