    def fillna(self, value, **kwargs):

        # allow filling with integers to be
        # interpreted as seconds
        if is_integer(value) and not isinstance(value, np.timedelta64):
            value = Timedelta(value, unit='s')
        return super(TimeDeltaBlock, self).fillna(value, **kwargs)
