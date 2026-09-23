    def to_datetime(self, dayfirst=False):
        """
        .. deprecated:: 0.19.0
           Use :meth:`to_timestamp` instead.

        Cast to DatetimeIndex.
        """
        warnings.warn("to_datetime is deprecated. Use self.to_timestamp(...)",
                      FutureWarning, stacklevel=2)
        return self.to_timestamp()
