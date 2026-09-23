    def _try_coerce_args(self, other):
        """
        Coerce other to dtype 'i8'. NaN and NaT convert to
        the smallest i8, and will correctly round-trip to NaT if converted
        back in _try_coerce_result. values is always ndarray-like, other
        may not be

        Parameters
        ----------
        other : ndarray-like or scalar

        Returns
        -------
        base-type other
        """
        if is_valid_nat_for_dtype(other, self.dtype):
            other = tslibs.iNaT
        elif is_integer(other) and other == tslibs.iNaT:
            pass
        elif isinstance(other, (datetime, np.datetime64, date)):
            other = self._box_func(other)
            if getattr(other, "tz") is not None:
                raise TypeError("cannot coerce a Timestamp with a tz on a naive Block")
            other = other.asm8.view("i8")
        elif hasattr(other, "dtype") and is_datetime64_dtype(other):
            other = other.astype("i8", copy=False).view("i8")
        else:
            # coercion issues
            # let higher levels handle
            raise TypeError(other)

        return other
