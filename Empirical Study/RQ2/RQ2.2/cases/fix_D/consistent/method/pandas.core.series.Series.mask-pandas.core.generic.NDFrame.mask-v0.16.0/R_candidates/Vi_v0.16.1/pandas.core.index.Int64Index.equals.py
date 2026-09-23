    def equals(self, other):
        """
        Determines if two Index objects contain the same elements.
        """
        if self.is_(other):
            return True

        # if not isinstance(other, Int64Index):
        #     return False

        try:
            return array_equivalent(_values_from_object(self), _values_from_object(other))
        except TypeError:
            # e.g. fails in numpy 1.6 with DatetimeIndex #1681
            return False
