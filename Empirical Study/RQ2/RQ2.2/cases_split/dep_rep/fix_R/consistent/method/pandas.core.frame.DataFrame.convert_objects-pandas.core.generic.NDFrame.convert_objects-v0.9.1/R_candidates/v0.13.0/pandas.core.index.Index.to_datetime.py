    def to_datetime(self, dayfirst=False):
        """
        For an Index containing strings or datetime.datetime objects, attempt
        conversion to DatetimeIndex
        """
        from pandas.tseries.index import DatetimeIndex
        if self.inferred_type == 'string':
            from dateutil.parser import parse
            parser = lambda x: parse(x, dayfirst=dayfirst)
            parsed = lib.try_parse_dates(self.values, parser=parser)
            return DatetimeIndex(parsed)
        else:
            return DatetimeIndex(self.values)
