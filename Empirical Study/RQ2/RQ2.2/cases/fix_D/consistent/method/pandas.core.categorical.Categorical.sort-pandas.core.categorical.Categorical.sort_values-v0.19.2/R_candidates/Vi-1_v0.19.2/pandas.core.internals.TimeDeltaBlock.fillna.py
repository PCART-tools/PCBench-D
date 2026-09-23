    def fillna(self, value, **kwargs):

        # allow filling with integers to be
        # interpreted as seconds
        if not isinstance(value, np.timedelta64) and is_integer(value):
            value = Timedelta(value, unit='s')
        return super(TimeDeltaBlock, self).fillna(value, **kwargs)
