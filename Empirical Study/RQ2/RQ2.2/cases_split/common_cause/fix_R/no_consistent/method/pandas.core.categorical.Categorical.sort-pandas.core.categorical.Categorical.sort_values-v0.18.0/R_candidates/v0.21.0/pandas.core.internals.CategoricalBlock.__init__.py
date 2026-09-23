    def __init__(self, values, placement, fastpath=False, **kwargs):

        # coerce to categorical if we can
        super(CategoricalBlock, self).__init__(_maybe_to_categorical(values),
                                               fastpath=True,
                                               placement=placement, **kwargs)
