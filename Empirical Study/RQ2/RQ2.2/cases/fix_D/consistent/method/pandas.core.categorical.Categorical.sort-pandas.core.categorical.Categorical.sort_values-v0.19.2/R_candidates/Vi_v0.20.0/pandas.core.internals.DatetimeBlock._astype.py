    def _astype(self, dtype, mgr=None, **kwargs):
        """
        these automatically copy, so copy=True has no effect
        raise on an except if raise == True
        """

        # if we are passed a datetime64[ns, tz]
        if is_datetime64tz_dtype(dtype):
            dtype = DatetimeTZDtype(dtype)

            values = self.values
            if getattr(values, 'tz', None) is None:
                values = DatetimeIndex(values).tz_localize('UTC')
            values = values.tz_convert(dtype.tz)
            return self.make_block(values)

        # delegate
        return super(DatetimeBlock, self)._astype(dtype=dtype, **kwargs)
