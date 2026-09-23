    def __init__(self, *args, **kwargs):
        # deprecation, #10892
        warnings.warn("WidePanel is deprecated. Please use Panel",
                      FutureWarning, stacklevel=2)

        super(WidePanel, self).__init__(*args, **kwargs)
