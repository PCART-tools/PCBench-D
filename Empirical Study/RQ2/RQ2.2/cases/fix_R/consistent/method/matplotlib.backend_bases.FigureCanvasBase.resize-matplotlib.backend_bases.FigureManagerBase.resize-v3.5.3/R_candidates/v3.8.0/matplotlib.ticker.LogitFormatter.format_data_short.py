    def format_data_short(self, value):
        # docstring inherited
        # Thresholds chosen to use scientific notation iff exponent <= -2.
        if value < 0.1:
            return f"{value:e}"
        if value < 0.9:
            return f"{value:f}"
        return f"1-{1 - value:e}"
