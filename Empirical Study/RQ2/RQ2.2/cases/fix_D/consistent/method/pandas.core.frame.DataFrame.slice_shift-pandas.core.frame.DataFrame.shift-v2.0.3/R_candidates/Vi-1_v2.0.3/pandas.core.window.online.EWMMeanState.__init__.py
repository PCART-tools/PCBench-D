    def __init__(self, com, adjust, ignore_na, axis, shape) -> None:
        alpha = 1.0 / (1.0 + com)
        self.axis = axis
        self.shape = shape
        self.adjust = adjust
        self.ignore_na = ignore_na
        self.new_wt = 1.0 if adjust else alpha
        self.old_wt_factor = 1.0 - alpha
        self.old_wt = np.ones(self.shape[self.axis - 1])
        self.last_ewm = None
