    def _try_coerce_args(self, values, other):
        """ provide coercion to our input arguments """

        if isinstance(other, ABCDatetimeIndex):
            # to store DatetimeTZBlock as object
            other = other.asobject.values

        return values, False, other, False
