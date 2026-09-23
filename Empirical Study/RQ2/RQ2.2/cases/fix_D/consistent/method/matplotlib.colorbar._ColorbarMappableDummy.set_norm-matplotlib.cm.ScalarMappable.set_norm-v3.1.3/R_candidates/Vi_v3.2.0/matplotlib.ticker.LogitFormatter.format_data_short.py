    def format_data_short(self, value):
        """
        Return a short formatted string representation of a number.
        """
        # thresholds choosen for use scienfic notation if and only if exponent
        # is less or equal than -2.
        if value < 0.1:
            return "{:e}".format(value)
        if value < 0.9:
            return "{:f}".format(value)
        return "1-{:e}".format(1 - value)
