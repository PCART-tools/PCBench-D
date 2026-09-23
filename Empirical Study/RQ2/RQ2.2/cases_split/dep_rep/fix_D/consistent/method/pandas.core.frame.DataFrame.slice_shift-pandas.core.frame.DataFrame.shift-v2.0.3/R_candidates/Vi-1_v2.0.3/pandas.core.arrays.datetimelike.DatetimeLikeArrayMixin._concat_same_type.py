    @classmethod
    def _concat_same_type(
        cls: type[DatetimeLikeArrayT],
        to_concat: Sequence[DatetimeLikeArrayT],
        axis: AxisInt = 0,
    ) -> DatetimeLikeArrayT:
        new_obj = super()._concat_same_type(to_concat, axis)

        obj = to_concat[0]
        dtype = obj.dtype

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

        new_obj._freq = new_freq
        return new_obj
