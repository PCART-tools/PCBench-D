    def _try_coerce_args(self, values, other):
        """ Coerce values and other to dtype 'i8'. NaN and NaT convert to
            the smallest i8, and will correctly round-trip to NaT if converted
            back in _try_coerce_result. values is always ndarray-like, other
            may not be """
        values = values.view('i8')

        if is_null_datelike_scalar(other):
            other = tslib.iNaT
        elif isinstance(other, datetime):
            other = lib.Timestamp(other).asm8.view('i8')
        elif hasattr(other, 'dtype') and com.is_integer_dtype(other):
            other = other.view('i8')
        else:
            other = np.array(other, dtype='i8')

        return values, other
