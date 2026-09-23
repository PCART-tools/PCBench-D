    def validate(self):
        if self.center is not None and not is_bool(self.center):
            raise ValueError("center must be a boolean")
        if self.min_periods is not None and not \
           is_integer(self.min_periods):
            raise ValueError("min_periods must be an integer")
