    @classmethod
    def _concat_same_type(cls, to_concat, axis: int = 0):

        # do not pass tz to set because tzlocal cannot be hashed
        dtypes = {str(x.dtype) for x in to_concat}
        if len(dtypes) != 1:
            raise ValueError("to_concat must have the same dtype (tz)", dtypes)

        obj = to_concat[0]
        dtype = obj.dtype

        i8values = [x.asi8 for x in to_concat]
        values = np.concatenate(i8values, axis=axis)

        new_freq = None
        if is_period_dtype(dtype):
            new_freq = obj.freq
        elif axis == 0:
            # GH 3232: If the concat result is evenly spaced, we can retain the
            # original frequency
            to_concat = [x for x in to_concat if len(x)]

            if obj.freq is not None and all(x.freq == obj.freq for x in to_concat):
                pairs = zip(to_concat[:-1], to_concat[1:])
                if all(pair[0][-1] + obj.freq == pair[1][0] for pair in pairs):
                    new_freq = obj.freq

        return cls._simple_new(values, dtype=dtype, freq=new_freq)
