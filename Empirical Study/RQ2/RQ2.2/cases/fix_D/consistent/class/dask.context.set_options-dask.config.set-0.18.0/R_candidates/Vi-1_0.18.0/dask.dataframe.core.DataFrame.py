class DataFrame(_Frame):
    """
    Parallel Pandas DataFrame

    Do not use this class directly.  Instead use functions like
    ``dd.read_csv``, ``dd.read_parquet``, or ``dd.from_pandas``.

    Parameters
    ----------
    dsk: dict
        The dask graph to compute this DataFrame
    name: str
        The key prefix that specifies which keys in the dask comprise this
        particular DataFrame
    meta: pandas.DataFrame
        An empty ``pandas.DataFrame`` with names, dtypes, and index matching
        the expected output.
    divisions: tuple of index values
        Values along which we partition our blocks on the index
    """

    _partition_type = pd.DataFrame
    _token_prefix = 'dataframe-'

    def __array_wrap__(self, array, context=None):
        if isinstance(context, tuple) and len(context) > 0:
            if isinstance(context[1][0], np.ndarray) and context[1][0].shape == ():
                index = None
            else:
                index = context[1][0].index

        return pd.DataFrame(array, index=index, columns=self.columns)

    @property
    def columns(self):
        return self._meta.columns

    @columns.setter
    def columns(self, columns):
        renamed = _rename_dask(self, columns)
        self._meta = renamed._meta
        self._name = renamed._name
        self.dask.update(renamed.dask)

    def __getitem__(self, key):
        name = 'getitem-%s' % tokenize(self, key)
        if np.isscalar(key) or isinstance(key, (tuple, string_types)):

            if isinstance(self._meta.index, (pd.DatetimeIndex, pd.PeriodIndex)):
                if key not in self._meta.columns:
                    return self.loc[key]

            # error is raised from pandas
            meta = self._meta[_extract_meta(key)]
            dsk = dict(((name, i), (operator.getitem, (self._name, i), key))
                       for i in range(self.npartitions))
            return new_dd_object(merge(self.dask, dsk), name,
                                 meta, self.divisions)
        elif isinstance(key, slice):
            return self.loc[key]

        if isinstance(key, (pd.Series, np.ndarray, pd.Index, list)):
            # error is raised from pandas
            meta = self._meta[_extract_meta(key)]

            dsk = dict(((name, i), (operator.getitem, (self._name, i), key))
                       for i in range(self.npartitions))
            return new_dd_object(merge(self.dask, dsk), name,
                                 meta, self.divisions)
        if isinstance(key, Series):
            # do not perform dummy calculation, as columns will not be changed.
            #
            if self.divisions != key.divisions:
                from .multi import _maybe_align_partitions
                self, key = _maybe_align_partitions([self, key])
            dsk = {(name, i): (M._getitem_array, (self._name, i), (key._name, i))
                   for i in range(self.npartitions)}
            return new_dd_object(merge(self.dask, key.dask, dsk), name,
                                 self, self.divisions)
        raise NotImplementedError(key)

    def __setitem__(self, key, value):
        if isinstance(key, (tuple, list)):
            df = self.assign(**{k: value[c]
                                for k, c in zip(key, value.columns)})
        else:
            df = self.assign(**{key: value})

        self.dask = df.dask
        self._name = df._name
        self._meta = df._meta
        self.divisions = df.divisions

    def __delitem__(self, key):
        result = self.drop([key], axis=1)
        self.dask = result.dask
        self._name = result._name
        self._meta = result._meta

    def __setattr__(self, key, value):
        try:
            columns = object.__getattribute__(self, '_meta').columns
        except AttributeError:
            columns = ()

        if key in columns:
            self[key] = value
        else:
            object.__setattr__(self, key, value)

    def __getattr__(self, key):
        if key in self.columns:
            meta = self._meta[key]
            name = 'getitem-%s' % tokenize(self, key)
            dsk = dict(((name, i), (operator.getitem, (self._name, i), key))
                       for i in range(self.npartitions))
            return new_dd_object(merge(self.dask, dsk), name,
                                 meta, self.divisions)
        raise AttributeError("'DataFrame' object has no attribute %r" % key)

    def __dir__(self):
        o = set(dir(type(self)))
        o.update(self.__dict__)
        o.update(c for c in self.columns if
                 (isinstance(c, pd.compat.string_types) and
                  pd.compat.isidentifier(c)))
        return list(o)

    @property
    def ndim(self):
        """ Return dimensionality """
        return 2

    @property
    def dtypes(self):
        """ Return data types """
        return self._meta.dtypes

    @derived_from(pd.DataFrame)
    def get_dtype_counts(self):
        return self._meta.get_dtype_counts()

    @derived_from(pd.DataFrame)
    def get_ftype_counts(self):
        return self._meta.get_ftype_counts()

    @derived_from(pd.DataFrame)
    def select_dtypes(self, include=None, exclude=None):
        cs = self._meta.select_dtypes(include=include, exclude=exclude).columns
        return self[list(cs)]

    def set_index(self, other, drop=True, sorted=False, npartitions=None,
                  divisions=None, **kwargs):
        """Set the DataFrame index (row labels) using an existing column

        This realigns the dataset to be sorted by a new column.  This can have a
        significant impact on performance, because joins, groupbys, lookups, etc.
        are all much faster on that column.  However, this performance increase
        comes with a cost, sorting a parallel dataset requires expensive shuffles.
        Often we ``set_index`` once directly after data ingest and filtering and
        then perform many cheap computations off of the sorted dataset.

        This function operates exactly like ``pandas.set_index`` except with
        different performance costs (it is much more expensive).  Under normal
        operation this function does an initial pass over the index column to
        compute approximate qunatiles to serve as future divisions.  It then passes
        over the data a second time, splitting up each input partition into several
        pieces and sharing those pieces to all of the output partitions now in
        sorted order.

        In some cases we can alleviate those costs, for example if your dataset is
        sorted already then we can avoid making many small pieces or if you know
        good values to split the new index column then we can avoid the initial
        pass over the data.  For example if your new index is a datetime index and
        your data is already sorted by day then this entire operation can be done
        for free.  You can control these options with the following parameters.

        Parameters
        ----------
        df: Dask DataFrame
        index: string or Dask Series
        npartitions: int, None, or 'auto'
            The ideal number of output partitions.   If None use the same as
            the input.  If 'auto' then decide by memory use.
        shuffle: string, optional
            Either ``'disk'`` for single-node operation or ``'tasks'`` for
            distributed operation.  Will be inferred by your current scheduler.
        sorted: bool, optional
            If the index column is already sorted in increasing order.
            Defaults to False
        divisions: list, optional
            Known values on which to separate index values of the partitions.
            See http://dask.pydata.org/en/latest/dataframe-design.html#partitions
            Defaults to computing this with a single pass over the data. Note
            that if ``sorted=True``, specified divisions are assumed to match
            the existing partitions in the data. If this is untrue, you should
            leave divisions empty and call ``repartition`` after ``set_index``.
        compute: bool
            Whether or not to trigger an immediate computation. Defaults to False.

        Examples
        --------
        >>> df2 = df.set_index('x')  # doctest: +SKIP
        >>> df2 = df.set_index(d.x)  # doctest: +SKIP
        >>> df2 = df.set_index(d.timestamp, sorted=True)  # doctest: +SKIP

        A common case is when we have a datetime column that we know to be
        sorted and is cleanly divided by day.  We can set this index for free
        by specifying both that the column is pre-sorted and the particular
        divisions along which is is separated

        >>> import pandas as pd
        >>> divisions = pd.date_range('2000', '2010', freq='1D')
        >>> df2 = df.set_index('timestamp', sorted=True, divisions=divisions)  # doctest: +SKIP
        """
        pre_sorted = sorted
        del sorted

        if divisions is not None:
            check_divisions(divisions)

        if pre_sorted:
            from .shuffle import set_sorted_index
            return set_sorted_index(self, other, drop=drop, divisions=divisions,
                                    **kwargs)
        else:
            from .shuffle import set_index
            return set_index(self, other, drop=drop, npartitions=npartitions,
                             divisions=divisions, **kwargs)

    @derived_from(pd.DataFrame)
    def nlargest(self, n=5, columns=None, split_every=None):
        token = 'dataframe-nlargest'
        return aca(self, chunk=M.nlargest, aggregate=M.nlargest,
                   meta=self._meta, token=token, split_every=split_every,
                   n=n, columns=columns)

    @derived_from(pd.DataFrame)
    def nsmallest(self, n=5, columns=None, split_every=None):
        token = 'dataframe-nsmallest'
        return aca(self, chunk=M.nsmallest, aggregate=M.nsmallest,
                   meta=self._meta, token=token, split_every=split_every,
                   n=n, columns=columns)

    @derived_from(pd.DataFrame)
    def groupby(self, by=None, **kwargs):
        from dask.dataframe.groupby import DataFrameGroupBy
        return DataFrameGroupBy(self, by=by, **kwargs)

    @wraps(categorize)
    def categorize(self, columns=None, index=None, split_every=None, **kwargs):
        return categorize(self, columns=columns, index=index,
                          split_every=split_every, **kwargs)

    @derived_from(pd.DataFrame)
    def assign(self, **kwargs):
        for k, v in kwargs.items():
            if not (isinstance(v, (Series, Scalar, pd.Series)) or
                    callable(v) or pd.api.types.is_scalar(v)):
                raise TypeError("Column assignment doesn't support type "
                                "{0}".format(type(v).__name__))
        pairs = list(sum(kwargs.items(), ()))

        # Figure out columns of the output
        df2 = self._meta.assign(**_extract_meta(kwargs))
        return elemwise(methods.assign, self, *pairs, meta=df2)

    @derived_from(pd.DataFrame, ua_args=['index'])
    def rename(self, index=None, columns=None):
        if index is not None:
            raise ValueError("Cannot rename index.")

        # *args here is index, columns but columns arg is already used
        return self.map_partitions(M.rename, None, columns=columns)

    def query(self, expr, **kwargs):
        """ Filter dataframe with complex expression

        Blocked version of pd.DataFrame.query

        This is like the sequential version except that this will also happen
        in many threads.  This may conflict with ``numexpr`` which will use
        multiple threads itself.  We recommend that you set numexpr to use a
        single thread

            import numexpr
            numexpr.set_nthreads(1)

        See also
        --------
        pandas.DataFrame.query
        """
        return self.map_partitions(M.query, expr, **kwargs)

    @derived_from(pd.DataFrame)
    def eval(self, expr, inplace=None, **kwargs):
        if inplace is None:
            if PANDAS_VERSION >= '0.21.0':
                inplace = False
        if '=' in expr and inplace in (True, None):
            raise NotImplementedError("Inplace eval not supported."
                                      " Please use inplace=False")
        meta = self._meta.eval(expr, inplace=inplace, **kwargs)
        return self.map_partitions(M.eval, expr, meta=meta, inplace=inplace, **kwargs)

    @derived_from(pd.DataFrame)
    def dropna(self, how='any', subset=None):
        return self.map_partitions(M.dropna, how=how, subset=subset)

    @derived_from(pd.DataFrame)
    def clip(self, lower=None, upper=None, out=None):
        if out is not None:
            raise ValueError("'out' must be None")
        return self.map_partitions(M.clip, lower=lower, upper=upper)

    @derived_from(pd.DataFrame)
    def clip_lower(self, threshold):
        return self.map_partitions(M.clip_lower, threshold=threshold)

    @derived_from(pd.DataFrame)
    def clip_upper(self, threshold):
        return self.map_partitions(M.clip_upper, threshold=threshold)

    @derived_from(pd.DataFrame)
    def squeeze(self, axis=None):
        if axis in [None, 1]:
            if len(self.columns) == 1:
                return self[self.columns[0]]
            else:
                return self

        elif axis == 0:
            raise NotImplementedError("{0} does not support "
                                      "squeeze along axis 0".format(type(self)))

        elif axis not in [0, 1, None]:
            raise ValueError('No axis {0} for object type {1}'.format(
                axis, type(self)))

    @derived_from(pd.DataFrame)
    def to_timestamp(self, freq=None, how='start', axis=0):
        df = elemwise(M.to_timestamp, self, freq, how, axis)
        df.divisions = tuple(pd.Index(self.divisions).to_timestamp())
        return df

    def to_bag(self, index=False):
        """Convert to a dask Bag of tuples of each row.

        Parameters
        ----------
        index : bool, optional
            If True, the index is included as the first element of each tuple.
            Default is False.
        """
        from .io import to_bag
        return to_bag(self, index)

    @derived_from(pd.DataFrame)
    def to_string(self, max_rows=5):
        # option_context doesn't affect
        return self._repr_data.to_string(max_rows=max_rows,
                                         show_dimensions=False)

    def _get_numeric_data(self, how='any', subset=None):
        # calculate columns to avoid unnecessary calculation
        numerics = self._meta._get_numeric_data()

        if len(numerics.columns) < len(self.columns):
            name = self._token_prefix + '-get_numeric_data'
            return self.map_partitions(M._get_numeric_data,
                                       meta=numerics, token=name)
        else:
            # use myself if all numerics
            return self

    @classmethod
    def _validate_axis(cls, axis=0):
        if axis not in (0, 1, 'index', 'columns', None):
            raise ValueError('No axis named {0}'.format(axis))
        # convert to numeric axis
        return {None: 0, 'index': 0, 'columns': 1}.get(axis, axis)

    @derived_from(pd.DataFrame)
    def drop(self, labels, axis=0, errors='raise'):
        axis = self._validate_axis(axis)
        if axis == 1:
            return self.map_partitions(M.drop, labels, axis=axis, errors=errors)
        raise NotImplementedError("Drop currently only works for axis=1")

    @derived_from(pd.DataFrame)
    def merge(self, right, how='inner', on=None, left_on=None, right_on=None,
              left_index=False, right_index=False, suffixes=('_x', '_y'),
              indicator=False, npartitions=None, shuffle=None):

        if not isinstance(right, (DataFrame, pd.DataFrame)):
            raise ValueError('right must be DataFrame')

        from .multi import merge
        return merge(self, right, how=how, on=on, left_on=left_on,
                     right_on=right_on, left_index=left_index,
                     right_index=right_index, suffixes=suffixes,
                     npartitions=npartitions, indicator=indicator,
                     shuffle=shuffle)

    @derived_from(pd.DataFrame)
    def join(self, other, on=None, how='left',
             lsuffix='', rsuffix='', npartitions=None, shuffle=None):

        if not isinstance(other, (DataFrame, pd.DataFrame)):
            raise ValueError('other must be DataFrame')

        from .multi import merge
        return merge(self, other, how=how,
                     left_index=on is None, right_index=True,
                     left_on=on, suffixes=[lsuffix, rsuffix],
                     npartitions=npartitions, shuffle=shuffle)

    @derived_from(pd.DataFrame)
    def append(self, other):
        if isinstance(other, Series):
            msg = ('Unable to appending dd.Series to dd.DataFrame.'
                   'Use pd.Series to append as row.')
            raise ValueError(msg)
        elif isinstance(other, pd.Series):
            other = other.to_frame().T
        return super(DataFrame, self).append(other)

    @derived_from(pd.DataFrame)
    def iterrows(self):
        for i in range(self.npartitions):
            df = self.get_partition(i).compute()
            for row in df.iterrows():
                yield row

    @derived_from(pd.DataFrame)
    def itertuples(self):
        for i in range(self.npartitions):
            df = self.get_partition(i).compute()
            for row in df.itertuples():
                yield row

    @classmethod
    def _bind_operator_method(cls, name, op):
        """ bind operator method like DataFrame.add to this class """

        # name must be explicitly passed for div method whose name is truediv

        def meth(self, other, axis='columns', level=None, fill_value=None):
            if level is not None:
                raise NotImplementedError('level must be None')

            axis = self._validate_axis(axis)

            if axis in (1, 'columns'):
                # When axis=1 and other is a series, `other` is transposed
                # and the operator is applied broadcast across rows. This
                # isn't supported with dd.Series.
                if isinstance(other, Series):
                    msg = 'Unable to {0} dd.Series with axis=1'.format(name)
                    raise ValueError(msg)
                elif isinstance(other, pd.Series):
                    # Special case for pd.Series to avoid unwanted partitioning
                    # of other. We pass it in as a kwarg to prevent this.
                    meta = _emulate(op, self, other=other, axis=axis,
                                    fill_value=fill_value)
                    return map_partitions(op, self, other=other, meta=meta,
                                          axis=axis, fill_value=fill_value)

            meta = _emulate(op, self, other, axis=axis, fill_value=fill_value)
            return map_partitions(op, self, other, meta=meta,
                                  axis=axis, fill_value=fill_value)
        meth.__doc__ = op.__doc__
        bind_method(cls, name, meth)

    @classmethod
    def _bind_comparison_method(cls, name, comparison):
        """ bind comparison method like DataFrame.add to this class """

        def meth(self, other, axis='columns', level=None):
            if level is not None:
                raise NotImplementedError('level must be None')
            axis = self._validate_axis(axis)
            return elemwise(comparison, self, other, axis=axis)

        meth.__doc__ = comparison.__doc__
        bind_method(cls, name, meth)

    @insert_meta_param_description(pad=12)
    def apply(self, func, axis=0, broadcast=None, raw=False, reduce=None,
              args=(), meta=no_default, **kwds):
        """ Parallel version of pandas.DataFrame.apply

        This mimics the pandas version except for the following:

        1.  Only ``axis=1`` is supported (and must be specified explicitly).
        2.  The user should provide output metadata via the `meta` keyword.

        Parameters
        ----------
        func : function
            Function to apply to each column/row
        axis : {0 or 'index', 1 or 'columns'}, default 0
            - 0 or 'index': apply function to each column (NOT SUPPORTED)
            - 1 or 'columns': apply function to each row
        $META
        args : tuple
            Positional arguments to pass to function in addition to the array/series

        Additional keyword arguments will be passed as keywords to the function

        Returns
        -------
        applied : Series or DataFrame

        Examples
        --------
        >>> import dask.dataframe as dd
        >>> df = pd.DataFrame({'x': [1, 2, 3, 4, 5],
        ...                    'y': [1., 2., 3., 4., 5.]})
        >>> ddf = dd.from_pandas(df, npartitions=2)

        Apply a function to row-wise passing in extra arguments in ``args`` and
        ``kwargs``:

        >>> def myadd(row, a, b=1):
        ...     return row.sum() + a + b
        >>> res = ddf.apply(myadd, axis=1, args=(2,), b=1.5)

        By default, dask tries to infer the output metadata by running your
        provided function on some fake data. This works well in many cases, but
        can sometimes be expensive, or even fail. To avoid this, you can
        manually specify the output metadata with the ``meta`` keyword. This
        can be specified in many forms, for more information see
        ``dask.dataframe.utils.make_meta``.

        Here we specify the output is a Series with name ``'x'``, and dtype
        ``float64``:

        >>> res = ddf.apply(myadd, axis=1, args=(2,), b=1.5, meta=('x', 'f8'))

        In the case where the metadata doesn't change, you can also pass in
        the object itself directly:

        >>> res = ddf.apply(lambda row: row + 1, axis=1, meta=ddf)

        See Also
        --------
        dask.DataFrame.map_partitions
        """

        axis = self._validate_axis(axis)
        pandas_kwargs = {
            'axis': axis,
            'broadcast': broadcast,
            'raw': raw,
            'reduce': None,
        }

        if PANDAS_VERSION >= '0.23.0':
            kwds.setdefault('result_type', None)

        kwds.update(pandas_kwargs)

        if axis == 0:
            msg = ("dd.DataFrame.apply only supports axis=1\n"
                   "  Try: df.apply(func, axis=1)")
            raise NotImplementedError(msg)

        if meta is no_default:
            msg = ("`meta` is not specified, inferred from partial data. "
                   "Please provide `meta` if the result is unexpected.\n"
                   "  Before: .apply(func)\n"
                   "  After:  .apply(func, meta={'x': 'f8', 'y': 'f8'}) for dataframe result\n"
                   "  or:     .apply(func, meta=('x', 'f8'))            for series result")
            warnings.warn(msg)

            meta = _emulate(M.apply, self._meta_nonempty, func,
                            args=args, udf=True, **kwds)

        return map_partitions(M.apply, self, func, args=args, meta=meta, **kwds)

    @derived_from(pd.DataFrame)
    def applymap(self, func, meta='__no_default__'):
        return elemwise(M.applymap, self, func, meta=meta)

    @derived_from(pd.DataFrame)
    def round(self, decimals=0):
        return elemwise(M.round, self, decimals)

    @derived_from(pd.DataFrame)
    def cov(self, min_periods=None, split_every=False):
        return cov_corr(self, min_periods, split_every=split_every)

    @derived_from(pd.DataFrame)
    def corr(self, method='pearson', min_periods=None, split_every=False):
        if method != 'pearson':
            raise NotImplementedError("Only Pearson correlation has been "
                                      "implemented")
        return cov_corr(self, min_periods, True, split_every=split_every)

    def info(self, buf=None, verbose=False, memory_usage=False):
        """
        Concise summary of a Dask DataFrame.
        """

        if buf is None:
            import sys
            buf = sys.stdout

        lines = [str(type(self))]

        if len(self.columns) == 0:
            lines.append('Index: 0 entries')
            lines.append('Empty %s' % type(self).__name__)
            put_lines(buf, lines)
            return

        # Group and execute the required computations
        computations = {}
        if verbose:
            computations.update({'index': self.index, 'count': self.count()})
        if memory_usage:
            computations.update({'memory_usage': self.map_partitions(M.memory_usage, index=True)})
        computations = dict(zip(computations.keys(), da.compute(*computations.values())))

        if verbose:
            index = computations['index']
            counts = computations['count']
            lines.append(index_summary(index))
            lines.append('Data columns (total {} columns):'.format(len(self.columns)))

            if PANDAS_VERSION >= '0.20.0':
                from pandas.io.formats.printing import pprint_thing
            else:
                from pandas.formats.printing import pprint_thing
            space = max([len(pprint_thing(k)) for k in self.columns]) + 3
            column_template = '{!s:<%d} {} non-null {}' % space
            column_info = [column_template.format(pprint_thing(x[0]), x[1], x[2])
                           for x in zip(self.columns, counts, self.dtypes)]
        else:
            column_info = [index_summary(self.columns, name='Columns')]

        lines.extend(column_info)
        dtype_counts = ['%s(%d)' % k for k in sorted(self.dtypes.value_counts().iteritems(), key=str)]
        lines.append('dtypes: {}'.format(', '.join(dtype_counts)))

        if memory_usage:
            memory_int = computations['memory_usage'].sum()
            lines.append('memory usage: {}\n'.format(memory_repr(memory_int)))

        put_lines(buf, lines)

    @derived_from(pd.DataFrame)
    def memory_usage(self, index=True, deep=False):
        result = self.map_partitions(M.memory_usage, index=index, deep=deep)
        result = result.groupby(result.index).sum()
        return result

    def pivot_table(self, index=None, columns=None,
                    values=None, aggfunc='mean'):
        """
        Create a spreadsheet-style pivot table as a DataFrame. Target ``columns``
        must have category dtype to infer result's ``columns``.
        ``index``, ``columns``, ``values`` and ``aggfunc`` must be all scalar.

        Parameters
        ----------
        values : scalar
            column to aggregate
        index : scalar
            column to be index
        columns : scalar
            column to be columns
        aggfunc : {'mean', 'sum', 'count'}, default 'mean'

        Returns
        -------
        table : DataFrame
        """
        from .reshape import pivot_table
        return pivot_table(self, index=index, columns=columns, values=values,
                           aggfunc=aggfunc)

    def to_records(self, index=False):
        from .io import to_records
        return to_records(self)

    @derived_from(pd.DataFrame)
    def to_html(self, max_rows=5):
        # pd.Series doesn't have html repr
        data = self._repr_data.to_html(max_rows=max_rows,
                                       show_dimensions=False)
        return self._HTML_FMT.format(data=data, name=key_split(self._name),
                                     task=len(self.dask))

    @property
    def _repr_data(self):
        meta = self._meta
        index = self._repr_divisions
        values = {c: _repr_data_series(meta[c], index) for c in meta.columns}
        return pd.DataFrame(values, columns=meta.columns)

    _HTML_FMT = """<div><strong>Dask DataFrame Structure:</strong></div>
{data}
<div>Dask Name: {name}, {task} tasks</div>"""

    def _repr_html_(self):
        data = self._repr_data.to_html(max_rows=5,
                                       show_dimensions=False, notebook=True)
        return self._HTML_FMT.format(data=data, name=key_split(self._name),
                                     task=len(self.dask))

    def _select_columns_or_index(self, columns_or_index):
        """
        Parameters
        ----------
        columns_or_index
            Column or index name, or a list of these

        Returns
        -------
        dd.DataFrame
            Dask DataFrame with columns corresponding to each column or
            index level in columns_or_index.  If included, the column
            corresponding to the index level is named _index
        """

        # Ensure columns_or_index is a list
        columns_or_index = (columns_or_index
                            if isinstance(columns_or_index, list)
                            else [columns_or_index])

        column_names = [n for n in columns_or_index if self._is_column_label_reference(n)]

        selected_df = self[column_names]
        if self._contains_index_name(columns_or_index):
            # Index name was included
            selected_df = selected_df.assign(_index=self.index)

        return selected_df

    def _is_column_label_reference(self, key):
        """
        Test whether a key is a column label reference

        To be considered a column label reference, `key` must match the name of at
        least one column.
        """
        return (not is_dask_collection(key) and
                (np.isscalar(key) or isinstance(key, tuple)) and
                key in self.columns)

    def _is_index_level_reference(self, key):
        """
        Test whether a key is an index level reference

        To be considered an index level reference, `key` must match the index name
        and must NOT match the name of any column.
        """
        return (self.index.name is not None and
                not is_dask_collection(key) and
                (np.isscalar(key) or isinstance(key, tuple)) and
                key == self.index.name and
                key not in self.columns)

    def _contains_index_name(self, columns_or_index):
        """
        Test whether the input contains a reference to the index of the DataFrame
        """
        if isinstance(columns_or_index, list):
            return any(self._is_index_level_reference(n) for n in columns_or_index)
        else:
            return self._is_index_level_reference(columns_or_index)
