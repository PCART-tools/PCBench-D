class _GroupBy(object):
    """ Superclass for DataFrameGroupBy and SeriesGroupBy

    Parameters
    ----------

    obj: DataFrame or Series
        DataFrame or Series to be grouped
    by: str, list or Series
        The key for grouping
    slice: str, list
        The slice keys applied to GroupBy result
    """
    def __init__(self, df, by=None, slice=None):

        assert isinstance(df, (DataFrame, Series))
        self.obj = df
        # grouping key passed via groupby method
        self.index = _normalize_index(df, by)

        if isinstance(self.index, list):
            do_index_partition_align = all(
                item.divisions == df.divisions if isinstance(item, Series) else True
                for item in self.index
            )
        elif isinstance(self.index, Series):
            do_index_partition_align = df.divisions == self.index.divisions
        else:
            do_index_partition_align = True

        if not do_index_partition_align:
            raise NotImplementedError("The grouped object and index of the "
                                      "groupby must have the same divisions.")

        # slicing key applied to _GroupBy instance
        self._slice = slice

        if isinstance(self.index, list):
            index_meta = [item._meta if isinstance(item, Series) else item for item in self.index]

        elif isinstance(self.index, Series):
            index_meta = self.index._meta

        else:
            index_meta = self.index

        self._meta = self.obj._meta.groupby(index_meta)

    @property
    def _meta_nonempty(self):
        """
        Return a pd.DataFrameGroupBy / pd.SeriesGroupBy which contains sample data.
        """
        sample = self.obj._meta_nonempty

        if isinstance(self.index, list):
            index_meta = [item._meta_nonempty if isinstance(item, Series) else item for item in self.index]

        elif isinstance(self.index, Series):
            index_meta = self.index._meta_nonempty

        else:
            index_meta = self.index

        grouped = sample.groupby(index_meta)
        return _maybe_slice(grouped, self._slice)

    def _aca_agg(self, token, func, aggfunc=None, split_every=None,
                 split_out=1):
        if aggfunc is None:
            aggfunc = func

        meta = func(self._meta)
        columns = meta.name if isinstance(meta, pd.Series) else meta.columns

        token = self._token_prefix + token
        levels = _determine_levels(self.index)

        return aca([self.obj, self.index] if not isinstance(self.index, list) else [self.obj] + self.index,
                   chunk=_apply_chunk,
                   chunk_kwargs=dict(chunk=func, columns=columns),
                   aggregate=_groupby_aggregate,
                   meta=meta, token=token, split_every=split_every,
                   aggregate_kwargs=dict(aggfunc=aggfunc, levels=levels),
                   split_out=split_out, split_out_setup=split_out_on_index)

    def _cum_agg(self, token, chunk, aggregate, initial):
        """ Wrapper for cumulative groupby operation """
        meta = chunk(self._meta)
        columns = meta.name if isinstance(meta, pd.Series) else meta.columns
        index = self.index if isinstance(self.index, list) else [self.index]

        name = self._token_prefix + token
        name_part = name + '-map'
        name_last = name + '-take-last'
        name_cum = name + '-cum-last'

        # cumulate each partitions
        cumpart_raw = map_partitions(_apply_chunk, self.obj, *index,
                                     chunk=chunk,
                                     columns=columns,
                                     token=name_part,
                                     meta=meta)

        cumpart_raw_frame = (cumpart_raw.to_frame()
                             if isinstance(meta, pd.Series)
                             else cumpart_raw)

        cumpart_ext = cumpart_raw_frame.assign(
            **{i: self.obj[i]
               if np.isscalar(i) and i in self.obj.columns
               else self.obj.index
               for i in index})

        # Use pd.Grouper objects to specify that we are grouping by columns.
        # Otherwise, pandas will throw an ambiguity warning if the
        # DataFrame's index (self.obj.index) was included in the grouping
        # specification (self.index). See pandas #14432
        index_groupers = [pd.Grouper(key=ind) for ind in index]
        cumlast = map_partitions(_apply_chunk, cumpart_ext, *index_groupers,
                                 columns=0 if columns is None else columns,
                                 chunk=M.last,
                                 meta=meta,
                                 token=name_last)

        # aggregate cumulated partisions and its previous last element
        dask = {}
        dask[(name, 0)] = (cumpart_raw._name, 0)

        for i in range(1, self.obj.npartitions):
            # store each cumulative step to graph to reduce computation
            if i == 1:
                dask[(name_cum, i)] = (cumlast._name, i - 1)
            else:
                # aggregate with previous cumulation results
                dask[(name_cum, i)] = (_cum_agg_filled,
                                       (name_cum, i - 1),
                                       (cumlast._name, i - 1),
                                       aggregate, initial)
            dask[(name, i)] = (_cum_agg_aligned,
                               (cumpart_ext._name, i), (name_cum, i),
                               index, 0 if columns is None else columns,
                               aggregate, initial)
        return new_dd_object(merge(dask, cumpart_ext.dask, cumlast.dask),
                             name, chunk(self._meta), self.obj.divisions)

    @derived_from(pd.core.groupby.GroupBy)
    def cumsum(self, axis=0):
        if axis:
            return self.obj.cumsum(axis=axis)
        else:
            return self._cum_agg('cumsum',
                                 chunk=M.cumsum,
                                 aggregate=M.add,
                                 initial=0)

    @derived_from(pd.core.groupby.GroupBy)
    def cumprod(self, axis=0):
        if axis:
            return self.obj.cumprod(axis=axis)
        else:
            return self._cum_agg('cumprod',
                                 chunk=M.cumprod,
                                 aggregate=M.mul,
                                 initial=1)

    @derived_from(pd.core.groupby.GroupBy)
    def cumcount(self, axis=None):
        return self._cum_agg('cumcount',
                             chunk=M.cumcount,
                             aggregate=_cumcount_aggregate,
                             initial=-1)

    @derived_from(pd.core.groupby.GroupBy)
    def sum(self, split_every=None, split_out=1):
        return self._aca_agg(token='sum', func=M.sum, split_every=split_every,
                             split_out=split_out)

    @derived_from(pd.core.groupby.GroupBy)
    def min(self, split_every=None, split_out=1):
        return self._aca_agg(token='min', func=M.min, split_every=split_every,
                             split_out=split_out)

    @derived_from(pd.core.groupby.GroupBy)
    def max(self, split_every=None, split_out=1):
        return self._aca_agg(token='max', func=M.max, split_every=split_every,
                             split_out=split_out)

    @derived_from(pd.core.groupby.GroupBy)
    def count(self, split_every=None, split_out=1):
        return self._aca_agg(token='count', func=M.count,
                             aggfunc=M.sum, split_every=split_every,
                             split_out=split_out)

    @derived_from(pd.core.groupby.GroupBy)
    def mean(self, split_every=None, split_out=1):
        return (self.sum(split_every=split_every, split_out=split_out) /
                self.count(split_every=split_every, split_out=split_out))

    @derived_from(pd.core.groupby.GroupBy)
    def size(self, split_every=None, split_out=1):
        return self._aca_agg(token='size', func=M.size, aggfunc=M.sum,
                             split_every=split_every, split_out=split_out)

    @derived_from(pd.core.groupby.GroupBy)
    def var(self, ddof=1, split_every=None, split_out=1):
        levels = _determine_levels(self.index)
        result = aca([self.obj, self.index] if not isinstance(self.index, list) else [self.obj] + self.index,
                     chunk=_var_chunk,
                     aggregate=_var_agg, combine=_var_combine,
                     token=self._token_prefix + 'var',
                     aggregate_kwargs={'ddof': ddof, 'levels': levels},
                     combine_kwargs={'levels': levels},
                     split_every=split_every, split_out=split_out,
                     split_out_setup=split_out_on_index)

        if isinstance(self.obj, Series):
            result = result[result.columns[0]]
        if self._slice:
            result = result[self._slice]

        return result

    @derived_from(pd.core.groupby.GroupBy)
    def std(self, ddof=1, split_every=None, split_out=1):
        v = self.var(ddof, split_every=split_every, split_out=split_out)
        result = map_partitions(np.sqrt, v, meta=v)
        return result

    @derived_from(pd.core.groupby.GroupBy)
    def first(self, split_every=None, split_out=1):
        return self._aca_agg(token='first', func=M.first, split_every=split_every,
                             split_out=split_out)

    @derived_from(pd.core.groupby.GroupBy)
    def last(self, split_every=None, split_out=1):
        return self._aca_agg(token='last', func=M.last, split_every=split_every,
                             split_out=split_out)

    @derived_from(pd.core.groupby.GroupBy)
    def get_group(self, key):
        token = self._token_prefix + 'get_group'

        meta = self._meta.obj
        if isinstance(meta, pd.DataFrame) and self._slice is not None:
            meta = meta[self._slice]
        columns = meta.columns if isinstance(meta, pd.DataFrame) else meta.name

        return map_partitions(_groupby_get_group, self.obj, self.index, key,
                              columns, meta=meta, token=token)

    def aggregate(self, arg, split_every, split_out=1):
        if isinstance(self.obj, DataFrame):
            if isinstance(self.index, tuple) or np.isscalar(self.index):
                group_columns = {self.index}

            elif isinstance(self.index, list):
                group_columns = {i for i in self.index
                                 if isinstance(i, tuple) or np.isscalar(i)}

            else:
                group_columns = set()

            if self._slice:
                # pandas doesn't exclude the grouping column in a SeriesGroupBy
                # like df.groupby('a')['a'].agg(...)
                non_group_columns = self._slice
                if not isinstance(non_group_columns, list):
                    non_group_columns = [non_group_columns]
            else:
                # NOTE: this step relies on the index normalization to replace
                #       series with their name in an index.
                non_group_columns = [col for col in self.obj.columns
                                     if col not in group_columns]

            spec = _normalize_spec(arg, non_group_columns)

        elif isinstance(self.obj, Series):
            if isinstance(arg, (list, tuple, dict)):
                # implementation detail: if self.obj is a series, a pseudo column
                # None is used to denote the series itself. This pseudo column is
                # removed from the result columns before passing the spec along.
                spec = _normalize_spec({None: arg}, [])
                spec = [(result_column, func, input_column)
                        for ((_, result_column), func, input_column) in spec]

            else:
                spec = _normalize_spec({None: arg}, [])
                spec = [(self.obj.name, func, input_column)
                        for (_, func, input_column) in spec]

        else:
            raise ValueError("aggregate on unknown object {}".format(self.obj))

        chunk_funcs, aggregate_funcs, finalizers = _build_agg_args(spec)

        if isinstance(self.index, (tuple, list)) and len(self.index) > 1:
            levels = list(range(len(self.index)))
        else:
            levels = 0

        if not isinstance(self.index, list):
            chunk_args = [self.obj, self.index]

        else:
            chunk_args = [self.obj] + self.index

        return aca(chunk_args,
                   chunk=_groupby_apply_funcs,
                   chunk_kwargs=dict(funcs=chunk_funcs),
                   combine=_groupby_apply_funcs,
                   combine_kwargs=dict(funcs=aggregate_funcs, level=levels),
                   aggregate=_agg_finalize,
                   aggregate_kwargs=dict(
                       aggregate_funcs=aggregate_funcs,
                       finalize_funcs=finalizers,
                       level=levels,
                   ),
                   token='aggregate', split_every=split_every,
                   split_out=split_out, split_out_setup=split_out_on_index)

    @insert_meta_param_description(pad=12)
    def apply(self, func, *args, **kwargs):
        """ Parallel version of pandas GroupBy.apply

        This mimics the pandas version except for the following:

        1.  The user should provide output metadata.
        2.  If the grouper does not align with the index then this causes a full
            shuffle.  The order of rows within each group may not be preserved.

        Parameters
        ----------
        func: function
            Function to apply
        args, kwargs : Scalar, Delayed or object
            Arguments and keywords to pass to the function.
        $META

        Returns
        -------
        applied : Series or DataFrame depending on columns keyword
        """
        meta = kwargs.get('meta', no_default)

        if meta is no_default:
            msg = ("`meta` is not specified, inferred from partial data. "
                   "Please provide `meta` if the result is unexpected.\n"
                   "  Before: .apply(func)\n"
                   "  After:  .apply(func, meta={'x': 'f8', 'y': 'f8'}) for dataframe result\n"
                   "  or:     .apply(func, meta=('x', 'f8'))            for series result")
            warnings.warn(msg, stacklevel=2)

            with raise_on_meta_error("groupby.apply({0})".format(funcname(func))):
                meta = self._meta_nonempty.apply(func, *args, **kwargs)

        meta = make_meta(meta)

        # Validate self.index
        if (isinstance(self.index, list) and
                any(isinstance(item, Series) for item in self.index)):
            raise NotImplementedError("groupby-apply with a multiple Series "
                                      "is currently not supported")

        df = self.obj
        should_shuffle = not (df.known_divisions and
                              df._contains_index_name(self.index))

        if should_shuffle:
            if isinstance(self.index, DataFrame):  # add index columns to dataframe
                df2 = df.assign(**{'_index_' + c: self.index[c]
                                   for c in self.index.columns})
                index = self.index
            elif isinstance(self.index, Series):
                df2 = df.assign(_index=self.index)
                index = self.index
            else:
                df2 = df
                index = df._select_columns_or_index(self.index)

            df3 = shuffle(df2, index)  # shuffle dataframe and index
        else:
            df3 = df

        if should_shuffle and isinstance(self.index, DataFrame):
            # extract index from dataframe
            cols = ['_index_' + c for c in self.index.columns]
            index2 = df3[cols]
            if isinstance(meta, pd.DataFrame):
                df4 = df3.map_partitions(drop_columns, cols, meta.columns.dtype)
            else:
                df4 = df3.drop(cols, axis=1)
        elif should_shuffle and isinstance(self.index, Series):
            index2 = df3['_index']
            index2.name = self.index.name
            if isinstance(meta, pd.DataFrame):
                df4 = df3.map_partitions(drop_columns, '_index',
                                         meta.columns.dtype)
            else:
                df4 = df3.drop('_index', axis=1)
        else:
            df4 = df3
            index2 = self.index

        # Perform embarrassingly parallel groupby-apply
        kwargs['meta'] = meta
        df5 = map_partitions(_groupby_slice_apply, df4, index2,
                             self._slice, func, *args, **kwargs)

        return df5
