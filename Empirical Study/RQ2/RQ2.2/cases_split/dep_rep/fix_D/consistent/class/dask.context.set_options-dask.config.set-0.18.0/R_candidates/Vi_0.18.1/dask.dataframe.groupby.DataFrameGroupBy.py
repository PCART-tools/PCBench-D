class DataFrameGroupBy(_GroupBy):

    _token_prefix = 'dataframe-groupby-'

    def __getitem__(self, key):
        if isinstance(key, list):
            g = DataFrameGroupBy(self.obj, by=self.index, slice=key)
        else:
            g = SeriesGroupBy(self.obj, by=self.index, slice=key)

        # error is raised from pandas
        g._meta = g._meta[key]
        return g

    def __dir__(self):
        return sorted(set(dir(type(self)) + list(self.__dict__) +
                      list(filter(pd.compat.isidentifier, self.obj.columns))))

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(e)

    @derived_from(pd.core.groupby.DataFrameGroupBy)
    def aggregate(self, arg, split_every=None, split_out=1):
        if arg == 'size':
            return self.size()

        return super(DataFrameGroupBy, self).aggregate(arg, split_every=split_every, split_out=split_out)

    @derived_from(pd.core.groupby.DataFrameGroupBy)
    def agg(self, arg, split_every=None, split_out=1):
        return self.aggregate(arg, split_every=split_every, split_out=split_out)
