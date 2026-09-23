    def _check_timedeltalike_freq_compat(self, other):
        """
        Arithmetic operations with timedelta-like scalars or array `other`
        are only valid if `other` is an integer multiple of `self.freq`.
        If the operation is valid, find that integer multiple.  Otherwise,
        raise because the operation is invalid.

        Parameters
        ----------
        other : timedelta, np.timedelta64, Tick,
                ndarray[timedelta64], TimedeltaArray, TimedeltaIndex

        Returns
        -------
        multiple : int or ndarray[int64]

        Raises
        ------
        IncompatibleFrequency
        """
        assert isinstance(self.freq, Tick)  # checked by calling function
        own_offset = frequencies.to_offset(self.freq.rule_code)
        base_nanos = delta_to_nanoseconds(own_offset)

        if isinstance(other, (timedelta, np.timedelta64, Tick)):
            nanos = delta_to_nanoseconds(other)

        elif isinstance(other, np.ndarray):
            # numpy timedelta64 array; all entries must be compatible
            assert other.dtype.kind == "m"
            if other.dtype != _TD_DTYPE:
                # i.e. non-nano unit
                # TODO: disallow unit-less timedelta64
                other = other.astype(_TD_DTYPE)
            nanos = other.view("i8")
        else:
            # TimedeltaArray/Index
            nanos = other.asi8

        if np.all(nanos % base_nanos == 0):
            # nanos being added is an integer multiple of the
            #  base-frequency to self.freq
            delta = nanos // base_nanos
            # delta is the integer (or integer-array) number of periods
            # by which will be added to self.
            return delta

        raise raise_on_incompatible(self, other)
