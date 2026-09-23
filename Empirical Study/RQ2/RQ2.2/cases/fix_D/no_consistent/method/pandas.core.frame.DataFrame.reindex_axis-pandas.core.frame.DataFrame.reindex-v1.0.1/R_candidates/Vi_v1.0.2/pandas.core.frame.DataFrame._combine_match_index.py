    def _combine_match_index(self, other, func):
        # at this point we have `self.index.equals(other.index)`

        if ops.should_series_dispatch(self, other, func):
            # operate column-wise; avoid costly object-casting in `.values`
            new_data = ops.dispatch_to_series(self, other, func)
        else:
            # fastpath --> operate directly on values
            with np.errstate(all="ignore"):
                new_data = func(self.values.T, other.values).T
        return new_data
