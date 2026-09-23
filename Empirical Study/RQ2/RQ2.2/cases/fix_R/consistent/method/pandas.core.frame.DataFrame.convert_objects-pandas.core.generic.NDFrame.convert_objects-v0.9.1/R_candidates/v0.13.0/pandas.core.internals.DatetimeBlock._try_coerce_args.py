    def _try_coerce_args(self, values, other):
        """ provide coercion to our input arguments
            we are going to compare vs i8, so coerce to integer
            values is always ndarra like, other may not be """
        values = values.view('i8')
        if isnull(other) or (np.isscalar(other) and other == tslib.iNaT):
            other = tslib.iNaT
        elif isinstance(other, datetime):
            other = lib.Timestamp(other).asm8.view('i8')
        else:
            other = other.view('i8')

        return values, other
