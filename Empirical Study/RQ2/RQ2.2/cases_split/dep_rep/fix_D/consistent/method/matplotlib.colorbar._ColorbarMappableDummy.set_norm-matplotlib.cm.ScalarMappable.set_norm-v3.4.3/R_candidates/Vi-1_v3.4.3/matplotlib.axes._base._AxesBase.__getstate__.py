    def __getstate__(self):
        # The renderer should be re-created by the figure, and then cached at
        # that point.
        state = super().__getstate__()
        # Prune the sharing & twinning info to only contain the current group.
        for grouper_name in [
                '_shared_x_axes', '_shared_y_axes', '_twinned_axes']:
            grouper = getattr(self, grouper_name)
            state[grouper_name] = (grouper.get_siblings(self)
                                   if self in grouper else None)
        return state
