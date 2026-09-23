    def __init__(self, obj, min_periods=1, freq=None, center=False, axis=0,
                 **kwargs):
        super(Expanding, self).__init__(obj=obj, min_periods=min_periods,
                                        freq=freq, center=center, axis=axis)
