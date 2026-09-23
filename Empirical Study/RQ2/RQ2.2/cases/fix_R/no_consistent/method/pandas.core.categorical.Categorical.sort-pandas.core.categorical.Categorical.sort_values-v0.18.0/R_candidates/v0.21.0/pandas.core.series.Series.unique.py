    @Appender(base._shared_docs['unique'] % _shared_doc_kwargs)
    def unique(self):
        result = super(Series, self).unique()

        if is_datetime64tz_dtype(self.dtype):
            # we are special casing datetime64tz_dtype
            # to return an object array of tz-aware Timestamps

            # TODO: it must return DatetimeArray with tz in pandas 2.0
            result = result.asobject.values

        return result
