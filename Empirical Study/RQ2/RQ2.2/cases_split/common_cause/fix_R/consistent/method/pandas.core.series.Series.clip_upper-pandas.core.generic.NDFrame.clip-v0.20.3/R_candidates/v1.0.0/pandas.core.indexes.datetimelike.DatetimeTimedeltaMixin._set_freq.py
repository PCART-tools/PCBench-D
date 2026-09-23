    def _set_freq(self, freq):
        """
        Set the _freq attribute on our underlying DatetimeArray.

        Parameters
        ----------
        freq : DateOffset, None, or "infer"
        """
        # GH#29843
        if freq is None:
            # Always valid
            pass
        elif len(self) == 0 and isinstance(freq, DateOffset):
            # Always valid.  In the TimedeltaIndex case, we assume this
            #  is a Tick offset.
            pass
        else:
            # As an internal method, we can ensure this assertion always holds
            assert freq == "infer"
            freq = to_offset(self.inferred_freq)

        self._data._freq = freq
