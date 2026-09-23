    def __init__(self, base=10.0, labelOnlyBase=False,
                 minor_thresholds=None,
                 linthresh=None):

        self._base = float(base)
        self.labelOnlyBase = labelOnlyBase
        if minor_thresholds is None:
            if rcParams['_internal.classic_mode']:
                minor_thresholds = (0, 0)
            else:
                minor_thresholds = (1, 0.4)
        self.minor_thresholds = minor_thresholds
        self._sublabels = None
        self._linthresh = linthresh
