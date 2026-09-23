    def format_data_short(self, value):
        # docstring inherited
        # Thresholds chosen to use scientific notation iff exponent <= -2.
        if value < 0.1:
            return "{:e}".format(value)
        if value < 0.9:
            return "{:f}".format(value)
        return "1-{:e}".format(1 - value)
