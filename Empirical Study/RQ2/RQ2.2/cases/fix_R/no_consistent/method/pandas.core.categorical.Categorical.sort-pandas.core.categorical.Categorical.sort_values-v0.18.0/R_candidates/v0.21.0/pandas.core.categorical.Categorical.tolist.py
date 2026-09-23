    def tolist(self):
        """
        Return a list of the values.

        These are each a scalar type, which is a Python scalar
        (for str, int, float) or a pandas scalar
        (for Timestamp/Timedelta/Interval/Period)
        """
        if is_datetimelike(self.categories):
            return [_maybe_box_datetimelike(x) for x in self]
        return np.array(self).tolist()
