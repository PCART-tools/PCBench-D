    def __init__(self, *args, **kwargs):
        # deprecation, #10892
        warnings.warn("LongPanel is deprecated. Please use DataFrame",
                      FutureWarning, stacklevel=2)

        super(LongPanel, self).__init__(*args, **kwargs)
