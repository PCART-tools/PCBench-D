    def _try_coerce_args(self, values, other):
        """ provide coercion to our input arguments """

        if np.any(notna(other)) and not self._can_hold_element(other):
            # coercion issues
            # let higher levels handle
            raise TypeError("cannot convert {} to an {}".format(
                type(other).__name__,
                type(self).__name__.lower().replace('Block', '')))

        return values, False, other, False
