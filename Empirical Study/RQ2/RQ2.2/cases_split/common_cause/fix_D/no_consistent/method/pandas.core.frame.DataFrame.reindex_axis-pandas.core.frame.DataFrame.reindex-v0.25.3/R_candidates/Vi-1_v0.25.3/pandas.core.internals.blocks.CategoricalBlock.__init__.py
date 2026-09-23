    def __init__(self, values, placement, ndim=None):
        from pandas.core.arrays.categorical import _maybe_to_categorical

        # coerce to categorical if we can
        super().__init__(_maybe_to_categorical(values), placement=placement, ndim=ndim)
