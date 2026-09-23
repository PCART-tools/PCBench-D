    @classmethod
    def _validate_frequency(cls, index, freq, **kwargs):
        """
        Validate that a frequency is compatible with the values of a given
        DatetimeIndex or TimedeltaIndex

        Parameters
        ----------
        index : DatetimeIndex or TimedeltaIndex
            The index on which to determine if the given frequency is valid
        freq : DateOffset
            The frequency to validate
        """
        inferred = index.inferred_freq
        if index.empty or inferred == freq.freqstr:
            return None

        on_freq = cls._generate(
            index[0], None, len(index), None, freq, **kwargs)
        if not np.array_equal(index.asi8, on_freq.asi8):
            msg = ('Inferred frequency {infer} from passed values does not '
                   'conform to passed frequency {passed}')
            raise ValueError(msg.format(infer=inferred, passed=freq.freqstr))
