    def to_datetime(self, dayfirst=False):
        """
        DEPRECATED: use :meth:`to_timestamp` instead.

        Cast to DatetimeIndex.
        """
        warnings.warn("to_datetime is deprecated. Use self.to_timestamp(...)",
                      FutureWarning, stacklevel=2)
        return self.to_timestamp()
