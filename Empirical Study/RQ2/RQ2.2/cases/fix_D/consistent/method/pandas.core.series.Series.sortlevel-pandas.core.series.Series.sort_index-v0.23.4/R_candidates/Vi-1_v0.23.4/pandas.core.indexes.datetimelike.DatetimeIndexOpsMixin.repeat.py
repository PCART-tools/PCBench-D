    def repeat(self, repeats, *args, **kwargs):
        """
        Analogous to ndarray.repeat
        """
        nv.validate_repeat(args, kwargs)
        if isinstance(self, ABCPeriodIndex):
            freq = self.freq
        else:
            freq = None
        return self._shallow_copy(self.asi8.repeat(repeats),
                                  freq=freq)
