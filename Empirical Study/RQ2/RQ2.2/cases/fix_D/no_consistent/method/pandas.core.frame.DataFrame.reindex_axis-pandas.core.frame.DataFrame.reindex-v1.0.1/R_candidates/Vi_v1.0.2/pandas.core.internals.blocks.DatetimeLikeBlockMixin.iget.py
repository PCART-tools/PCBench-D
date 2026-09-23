    def iget(self, key):
        # GH#31649 we need to wrap scalars in Timestamp/Timedelta
        # TODO(EA2D): this can be removed if we ever have 2D EA
        result = super().iget(key)
        if isinstance(result, np.datetime64):
            result = Timestamp(result)
        elif isinstance(result, np.timedelta64):
            result = Timedelta(result)
        return result
