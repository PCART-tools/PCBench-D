    def to_datetime(self, dayfirst=False):
        """
        DEPRECATED: use :meth:`pandas.to_datetime` instead.

        For an Index containing strings or datetime.datetime objects, attempt
        conversion to DatetimeIndex
        """
        warnings.warn("to_datetime is deprecated. Use pd.to_datetime(...)",
                      FutureWarning, stacklevel=2)

        from pandas.core.indexes.datetimes import DatetimeIndex
        if self.inferred_type == 'string':
            from dateutil.parser import parse
            parser = lambda x: parse(x, dayfirst=dayfirst)
            parsed = lib.try_parse_dates(self.values, parser=parser)
            return DatetimeIndex(parsed)
        else:
            return DatetimeIndex(self.values)
