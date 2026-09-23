    def __init__(self, *args, **kwargs):
        # deprecation TimeSeries, #10890
        warnings.warn("TimeSeries is deprecated. Please use Series",
                      FutureWarning, stacklevel=2)

        super(TimeSeries, self).__init__(*args, **kwargs)
