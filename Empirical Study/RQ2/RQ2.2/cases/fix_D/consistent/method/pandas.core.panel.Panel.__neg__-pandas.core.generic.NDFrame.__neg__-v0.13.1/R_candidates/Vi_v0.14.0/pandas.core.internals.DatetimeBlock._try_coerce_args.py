    def _try_coerce_args(self, values, other):
        """ provide coercion to our input arguments
            we are going to compare vs i8, so coerce to integer
            values is always ndarra like, other may not be """
        values = values.view('i8')
        if _is_null_datelike_scalar(other):
            other = tslib.iNaT
        elif isinstance(other, datetime):
            other = lib.Timestamp(other).asm8.view('i8')
        else:
            other = other.view('i8')

        return values, other
