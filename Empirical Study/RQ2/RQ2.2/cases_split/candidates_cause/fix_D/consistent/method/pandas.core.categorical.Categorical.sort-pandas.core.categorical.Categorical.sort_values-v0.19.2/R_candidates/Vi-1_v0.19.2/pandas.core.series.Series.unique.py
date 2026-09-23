    @Appender(base._shared_docs['unique'] % _shared_doc_kwargs)
    def unique(self):
        result = super(Series, self).unique()
        if is_datetime64tz_dtype(self.dtype):
            # to return array of Timestamp with tz
            # ToDo: it must return DatetimeArray with tz in pandas 2.0
            return result.asobject.values
        return result
