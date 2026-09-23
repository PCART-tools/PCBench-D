class SeriesGroupBy(_GroupBy):

    _token_prefix = 'series-groupby-'

    def __init__(self, df, by=None, slice=None):
        # for any non series object, raise pandas-compat error message

        if isinstance(df, Series):
            if isinstance(by, Series):
                pass
            elif isinstance(by, list):
                if len(by) == 0:
                    raise ValueError("No group keys passed!")

                non_series_items = [item for item in by
                                    if not isinstance(item, Series)]
                # raise error from pandas, if applicable
                df._meta.groupby(non_series_items)
            else:
                # raise error from pandas, if applicable
                df._meta.groupby(by)

        super(SeriesGroupBy, self).__init__(df, by=by, slice=slice)

    def nunique(self, split_every=None, split_out=1):
        name = self._meta.obj.name
        levels = _determine_levels(self.index)

        if isinstance(self.obj, DataFrame):
            chunk = _nunique_df_chunk

        else:
            chunk = _nunique_series_chunk

        return aca([self.obj, self.index] if not isinstance(self.index, list) else [self.obj] + self.index,
                   chunk=chunk,
                   aggregate=_nunique_df_aggregate,
                   combine=_nunique_df_combine,
                   token='series-groupby-nunique',
                   chunk_kwargs={'levels': levels, 'name': name},
                   aggregate_kwargs={'levels': levels, 'name': name},
                   combine_kwargs={'levels': levels},
                   split_every=split_every, split_out=split_out,
                   split_out_setup=split_out_on_index)

    @derived_from(pd.core.groupby.SeriesGroupBy)
    def aggregate(self, arg, split_every=None, split_out=1):
        result = super(SeriesGroupBy, self).aggregate(arg, split_every=split_every, split_out=split_out)
        if self._slice:
            result = result[self._slice]

        if not isinstance(arg, (list, dict)) and isinstance(result, DataFrame):
            result = result[result.columns[0]]

        return result

    @derived_from(pd.core.groupby.SeriesGroupBy)
    def agg(self, arg, split_every=None, split_out=1):
        return self.aggregate(arg, split_every=split_every, split_out=split_out)
