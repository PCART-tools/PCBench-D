    def _addsub_offset_array(self, other, op):
        # Add or subtract Array-like of DateOffset objects
        try:
            # TimedeltaIndex can only operate with a subset of DateOffset
            # subclasses.  Incompatible classes will raise AttributeError,
            # which we re-raise as TypeError
            return DatetimeIndexOpsMixin._addsub_offset_array(self, other, op)
        except AttributeError:
            raise TypeError("Cannot add/subtract non-tick DateOffset to {cls}"
                            .format(cls=type(self).__name__))
