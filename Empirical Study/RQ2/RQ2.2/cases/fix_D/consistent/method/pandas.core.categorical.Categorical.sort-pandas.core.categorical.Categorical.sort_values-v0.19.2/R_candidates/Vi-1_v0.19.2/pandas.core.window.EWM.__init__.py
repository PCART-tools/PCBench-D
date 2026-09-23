    def __init__(self, obj, com=None, span=None, halflife=None, alpha=None,
                 min_periods=0, freq=None, adjust=True, ignore_na=False,
                 axis=0):
        self.obj = obj
        self.com = _get_center_of_mass(com, span, halflife, alpha)
        self.min_periods = min_periods
        self.freq = freq
        self.adjust = adjust
        self.ignore_na = ignore_na
        self.axis = axis
        self.on = None
