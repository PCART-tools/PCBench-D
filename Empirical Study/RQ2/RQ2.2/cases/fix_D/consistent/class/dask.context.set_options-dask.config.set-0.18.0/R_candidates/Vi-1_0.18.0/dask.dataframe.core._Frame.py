class _Frame(DaskMethodsMixin, OperatorMethodMixin):
    """ Superclass for DataFrame and Series

    Parameters
    ----------

    dsk: dict
        The dask graph to compute this DataFrame
    name: str
        The key prefix that specifies which keys in the dask comprise this
        particular DataFrame / Series
    meta: pandas.DataFrame, pandas.Series, or pandas.Index
        An empty pandas object with names, dtypes, and indices matching the
        expected output.
    divisions: tuple of index values
        Values along which we partition our blocks on the index
    """
    def __init__(self, dsk, name, meta, divisions):
        self.dask = dsk
        self._name = name
        meta = make_meta(meta)
        if not isinstance(meta, self._partition_type):
            raise TypeError("Expected meta to specify type {0}, got type "
                            "{1}".format(self._partition_type.__name__,
                                         type(meta).__name__))
        self._meta = meta
        self.divisions = tuple(divisions)

    def __dask_graph__(self):
        return self.dask

    def __dask_keys__(self):
        return [(self._name, i) for i in range(self.npartitions)]

    def __dask_tokenize__(self):
        return self._name

    __dask_optimize__ = globalmethod(optimize, key='dataframe_optimize',
                                     falsey=dont_optimize)
    __dask_scheduler__ = staticmethod(threaded.get)

    def __dask_postcompute__(self):
        return finalize, ()

    def __dask_postpersist__(self):
        return type(self), (self._name, self._meta, self.divisions)

    @property
    def _constructor(self):
        return new_dd_object

    @property
    def npartitions(self):
        """Return number of partitions"""
        return len(self.divisions) - 1

    @property
    def size(self):
        """ Size of the series """
        return self.reduction(methods.size, np.sum, token='size', meta=int,
                              split_every=False)

    @property
    def _meta_nonempty(self):
        """ A non-empty version of `_meta` with fake data."""
        return meta_nonempty(self._meta)

    @property
    def _args(self):
        return (self.dask, self._name, self._meta, self.divisions)

    def __getstate__(self):
        return self._args

    def __setstate__(self, state):
        self.dask, self._name, self._meta, self.divisions = state

    def copy(self):
        """ Make a copy of the dataframe

        This is strictly a shallow copy of the underlying computational graph.
        It does not affect the underlying data
        """
        return new_dd_object(self.dask, self._name,
                             self._meta, self.divisions)

    def __array__(self, dtype=None, **kwargs):
        self._computed = self.compute()
        x = np.array(self._computed)
        return x

    def __array_wrap__(self, array, context=None):
        raise NotImplementedError

    def __array_ufunc__(self, numpy_ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            # ufuncs work with 0-dimensional NumPy ndarrays
            # so we don't want to raise NotImplemented
            if isinstance(x, np.ndarray) and x.shape == ():
                continue
            elif not isinstance(x, (Number, Scalar, _Frame, Array,
                                    pd.DataFrame, pd.Series, pd.Index)):
                return NotImplemented

        if method == '__call__':
            if numpy_ufunc.signature is not None:
                return NotImplemented
            if numpy_ufunc.nout > 1:
                # ufuncs with multiple output values
                # are not yet supported for frames
                return NotImplemented
            else:
                return elemwise(numpy_ufunc, *inputs, **kwargs)
        else:
            # ufunc methods are not yet supported for frames
            return NotImplemented

    @property
    def _elemwise(self):
        return elemwise

    @property
    def _repr_data(self):
        raise NotImplementedError

    @property
    def _repr_divisions(self):
        name = "npartitions={0}".format(self.npartitions)
        if self.known_divisions:
            divisions = pd.Index(self.divisions, name=name)
        else:
            # avoid to be converted to NaN
            divisions = pd.Index([''] * (self.npartitions + 1), name=name)
        return divisions

    def __repr__(self):
        data = self._repr_data.to_string(max_rows=5, show_dimensions=False)
        return """Dask {klass} Structure:
{data}
Dask Name: {name}, {task} tasks""".format(klass=self.__class__.__name__,
                                          data=data, name=key_split(self._name),
                                          task=len(self.dask))

    @property
    def index(self):
        """Return dask Index instance"""
        name = self._name + '-index'
        dsk = {(name, i): (getattr, key, 'index')
               for i, key in enumerate(self.__dask_keys__())}

        return Index(merge(dsk, self.dask), name,
                     self._meta.index, self.divisions)

    def reset_index(self, drop=False):
        """Reset the index to the default index.

        Note that unlike in ``pandas``, the reset ``dask.dataframe`` index will
        not be monotonically increasing from 0. Instead, it will restart at 0
        for each partition (e.g. ``index1 = [0, ..., 10], index2 = [0, ...]``).
        This is due to the inability to statically know the full length of the
        index.

        For DataFrame with multi-level index, returns a new DataFrame with
        labeling information in the columns under the index names, defaulting
        to 'level_0', 'level_1', etc. if any are None. For a standard index,
        the index name will be used (if set), otherwise a default 'index' or
        'level_0' (if 'index' is already taken) will be used.

        Parameters
        ----------
        drop : boolean, default False
            Do not try to insert index into dataframe columns.
        """
        return self.map_partitions(M.reset_index, drop=drop).clear_divisions()

    @property
    def known_divisions(self):
        """Whether divisions are already known"""
        return len(self.divisions) > 0 and self.divisions[0] is not None

    def clear_divisions(self):
        """ Forget division information """
        divisions = (None,) * (self.npartitions + 1)
        return type(self)(self.dask, self._name, self._meta, divisions)

    def get_partition(self, n):
        """Get a dask DataFrame/Series representing the `nth` partition."""
        if 0 <= n < self.npartitions:
            name = 'get-partition-%s-%s' % (str(n), self._name)
            dsk = {(name, 0): (self._name, n)}
            divisions = self.divisions[n:n + 2]
            return new_dd_object(merge(self.dask, dsk), name,
                                 self._meta, divisions)
        else:
            msg = "n must be 0 <= n < {0}".format(self.npartitions)
            raise ValueError(msg)

    @derived_from(pd.DataFrame)
    def drop_duplicates(self, split_every=None, split_out=1, **kwargs):
        # Let pandas error on bad inputs
        self._meta_nonempty.drop_duplicates(**kwargs)
        if 'subset' in kwargs and kwargs['subset'] is not None:
            split_out_setup = split_out_on_cols
            split_out_setup_kwargs = {'cols': kwargs['subset']}
        else:
            split_out_setup = split_out_setup_kwargs = None

        if kwargs.get('keep', True) is False:
            raise NotImplementedError("drop_duplicates with keep=False")

        chunk = M.drop_duplicates
        return aca(self, chunk=chunk, aggregate=chunk, meta=self._meta,
                   token='drop-duplicates', split_every=split_every,
                   split_out=split_out, split_out_setup=split_out_setup,
                   split_out_setup_kwargs=split_out_setup_kwargs, **kwargs)

    def __len__(self):
        return self.reduction(len, np.sum, token='len', meta=int,
                              split_every=False).compute()

    def __bool__(self):
        raise ValueError("The truth value of a {0} is ambiguous. "
                         "Use a.any() or a.all()."
                         .format(self.__class__.__name__))

    __nonzero__ = __bool__  # python 2

    def _scalarfunc(self, cast_type):
        def wrapper():
            raise TypeError("cannot convert the series to "
                            "{0}".format(str(cast_type)))

        return wrapper

    def __float__(self):
        return self._scalarfunc(float)

    def __int__(self):
        return self._scalarfunc(int)

    __long__ = __int__  # python 2

    def __complex__(self):
        return self._scalarfunc(complex)

    @insert_meta_param_description(pad=12)
    def map_partitions(self, func, *args, **kwargs):
        """ Apply Python function on each DataFrame partition.

        Note that the index and divisions are assumed to remain unchanged.

        Parameters
        ----------
        func : function
            Function applied to each partition.
        args, kwargs :
            Arguments and keywords to pass to the function. The partition will
            be the first argument, and these will be passed *after*. Arguments
            and keywords may contain ``Scalar``, ``Delayed`` or regular
            python objects.
        $META

        Examples
        --------
        Given a DataFrame, Series, or Index, such as:

        >>> import dask.dataframe as dd
        >>> df = pd.DataFrame({'x': [1, 2, 3, 4, 5],
        ...                    'y': [1., 2., 3., 4., 5.]})
        >>> ddf = dd.from_pandas(df, npartitions=2)

        One can use ``map_partitions`` to apply a function on each partition.
        Extra arguments and keywords can optionally be provided, and will be
        passed to the function after the partition.

        Here we apply a function with arguments and keywords to a DataFrame,
        resulting in a Series:

        >>> def myadd(df, a, b=1):
        ...     return df.x + df.y + a + b
        >>> res = ddf.map_partitions(myadd, 1, b=2)
        >>> res.dtype
        dtype('float64')

        By default, dask tries to infer the output metadata by running your
        provided function on some fake data. This works well in many cases, but
        can sometimes be expensive, or even fail. To avoid this, you can
        manually specify the output metadata with the ``meta`` keyword. This
        can be specified in many forms, for more information see
        ``dask.dataframe.utils.make_meta``.

        Here we specify the output is a Series with no name, and dtype
        ``float64``:

        >>> res = ddf.map_partitions(myadd, 1, b=2, meta=(None, 'f8'))

        Here we map a function that takes in a DataFrame, and returns a
        DataFrame with a new column:

        >>> res = ddf.map_partitions(lambda df: df.assign(z=df.x * df.y))
        >>> res.dtypes
        x      int64
        y    float64
        z    float64
        dtype: object

        As before, the output metadata can also be specified manually. This
        time we pass in a ``dict``, as the output is a DataFrame:

        >>> res = ddf.map_partitions(lambda df: df.assign(z=df.x * df.y),
        ...                          meta={'x': 'i8', 'y': 'f8', 'z': 'f8'})

        In the case where the metadata doesn't change, you can also pass in
        the object itself directly:

        >>> res = ddf.map_partitions(lambda df: df.head(), meta=df)

        Also note that the index and divisions are assumed to remain unchanged.
        If the function you're mapping changes the index/divisions, you'll need
        to clear them afterwards:

        >>> ddf.map_partitions(func).clear_divisions()  # doctest: +SKIP
        """
        return map_partitions(func, self, *args, **kwargs)

    @insert_meta_param_description(pad=12)
    def map_overlap(self, func, before, after, *args, **kwargs):
        """Apply a function to each partition, sharing rows with adjacent partitions.

        This can be useful for implementing windowing functions such as
        ``df.rolling(...).mean()`` or ``df.diff()``.

        Parameters
        ----------
        func : function
            Function applied to each partition.
        before : int
            The number of rows to prepend to partition ``i`` from the end of
            partition ``i - 1``.
        after : int
            The number of rows to append to partition ``i`` from the beginning
            of partition ``i + 1``.
        args, kwargs :
            Arguments and keywords to pass to the function. The partition will
            be the first argument, and these will be passed *after*.
        $META

        Notes
        -----
        Given positive integers ``before`` and ``after``, and a function
        ``func``, ``map_overlap`` does the following:

        1. Prepend ``before`` rows to each partition ``i`` from the end of
           partition ``i - 1``. The first partition has no rows prepended.

        2. Append ``after`` rows to each partition ``i`` from the beginning of
           partition ``i + 1``. The last partition has no rows appended.

        3. Apply ``func`` to each partition, passing in any extra ``args`` and
           ``kwargs`` if provided.

        4. Trim ``before`` rows from the beginning of all but the first
           partition.

        5. Trim ``after`` rows from the end of all but the last partition.

        Note that the index and divisions are assumed to remain unchanged.

        Examples
        --------
        Given a DataFrame, Series, or Index, such as:

        >>> import dask.dataframe as dd
        >>> df = pd.DataFrame({'x': [1, 2, 4, 7, 11],
        ...                    'y': [1., 2., 3., 4., 5.]})
        >>> ddf = dd.from_pandas(df, npartitions=2)

        A rolling sum with a trailing moving window of size 2 can be computed by
        overlapping 2 rows before each partition, and then mapping calls to
        ``df.rolling(2).sum()``:

        >>> ddf.compute()
            x    y
        0   1  1.0
        1   2  2.0
        2   4  3.0
        3   7  4.0
        4  11  5.0
        >>> ddf.map_overlap(lambda df: df.rolling(2).sum(), 2, 0).compute()
              x    y
        0   NaN  NaN
        1   3.0  3.0
        2   6.0  5.0
        3  11.0  7.0
        4  18.0  9.0

        The pandas ``diff`` method computes a discrete difference shifted by a
        number of periods (can be positive or negative). This can be
        implemented by mapping calls to ``df.diff`` to each partition after
        prepending/appending that many rows, depending on sign:

        >>> def diff(df, periods=1):
        ...     before, after = (periods, 0) if periods > 0 else (0, -periods)
        ...     return df.map_overlap(lambda df, periods=1: df.diff(periods),
        ...                           periods, 0, periods=periods)
        >>> diff(ddf, 1).compute()
             x    y
        0  NaN  NaN
        1  1.0  1.0
        2  2.0  1.0
        3  3.0  1.0
        4  4.0  1.0

        If you have a ``DatetimeIndex``, you can use a ``pd.Timedelta`` for time-
        based windows.

        >>> ts = pd.Series(range(10), index=pd.date_range('2017', periods=10))
        >>> dts = dd.from_pandas(ts, npartitions=2)
        >>> dts.map_overlap(lambda df: df.rolling('2D').sum(),
        ...                 pd.Timedelta('2D'), 0).compute()
        2017-01-01     0.0
        2017-01-02     1.0
        2017-01-03     3.0
        2017-01-04     5.0
        2017-01-05     7.0
        2017-01-06     9.0
        2017-01-07    11.0
        2017-01-08    13.0
        2017-01-09    15.0
        2017-01-10    17.0
        dtype: float64
        """
        from .rolling import map_overlap
        return map_overlap(func, self, before, after, *args, **kwargs)

    @insert_meta_param_description(pad=12)
    def reduction(self, chunk, aggregate=None, combine=None, meta=no_default,
                  token=None, split_every=None, chunk_kwargs=None,
                  aggregate_kwargs=None, combine_kwargs=None, **kwargs):
        """Generic row-wise reductions.

        Parameters
        ----------
        chunk : callable
            Function to operate on each partition. Should return a
            ``pandas.DataFrame``, ``pandas.Series``, or a scalar.
        aggregate : callable, optional
            Function to operate on the concatenated result of ``chunk``. If not
            specified, defaults to ``chunk``. Used to do the final aggregation
            in a tree reduction.

            The input to ``aggregate`` depends on the output of ``chunk``.
            If the output of ``chunk`` is a:

            - scalar: Input is a Series, with one row per partition.
            - Series: Input is a DataFrame, with one row per partition. Columns
              are the rows in the output series.
            - DataFrame: Input is a DataFrame, with one row per partition.
              Columns are the columns in the output dataframes.

            Should return a ``pandas.DataFrame``, ``pandas.Series``, or a
            scalar.
        combine : callable, optional
            Function to operate on intermediate concatenated results of
            ``chunk`` in a tree-reduction. If not provided, defaults to
            ``aggregate``. The input/output requirements should match that of
            ``aggregate`` described above.
        $META
        token : str, optional
            The name to use for the output keys.
        split_every : int, optional
            Group partitions into groups of this size while performing a
            tree-reduction. If set to False, no tree-reduction will be used,
            and all intermediates will be concatenated and passed to
            ``aggregate``. Default is 8.
        chunk_kwargs : dict, optional
            Keyword arguments to pass on to ``chunk`` only.
        aggregate_kwargs : dict, optional
            Keyword arguments to pass on to ``aggregate`` only.
        combine_kwargs : dict, optional
            Keyword arguments to pass on to ``combine`` only.
        kwargs :
            All remaining keywords will be passed to ``chunk``, ``combine``,
            and ``aggregate``.

        Examples
        --------
        >>> import pandas as pd
        >>> import dask.dataframe as dd
        >>> df = pd.DataFrame({'x': range(50), 'y': range(50, 100)})
        >>> ddf = dd.from_pandas(df, npartitions=4)

        Count the number of rows in a DataFrame. To do this, count the number
        of rows in each partition, then sum the results:

        >>> res = ddf.reduction(lambda x: x.count(),
        ...                     aggregate=lambda x: x.sum())
        >>> res.compute()
        x    50
        y    50
        dtype: int64

        Count the number of rows in a Series with elements greater than or
        equal to a value (provided via a keyword).

        >>> def count_greater(x, value=0):
        ...     return (x >= value).sum()
        >>> res = ddf.x.reduction(count_greater, aggregate=lambda x: x.sum(),
        ...                       chunk_kwargs={'value': 25})
        >>> res.compute()
        25

        Aggregate both the sum and count of a Series at the same time:

        >>> def sum_and_count(x):
        ...     return pd.Series({'sum': x.sum(), 'count': x.count()})
        >>> res = ddf.x.reduction(sum_and_count, aggregate=lambda x: x.sum())
        >>> res.compute()
        count      50
        sum      1225
        dtype: int64

        Doing the same, but for a DataFrame. Here ``chunk`` returns a
        DataFrame, meaning the input to ``aggregate`` is a DataFrame with an
        index with non-unique entries for both 'x' and 'y'. We groupby the
        index, and sum each group to get the final result.

        >>> def sum_and_count(x):
        ...     return pd.DataFrame({'sum': x.sum(), 'count': x.count()})
        >>> res = ddf.reduction(sum_and_count,
        ...                     aggregate=lambda x: x.groupby(level=0).sum())
        >>> res.compute()
           count   sum
        x     50  1225
        y     50  3725
        """
        if aggregate is None:
            aggregate = chunk

        if combine is None:
            if combine_kwargs:
                raise ValueError("`combine_kwargs` provided with no `combine`")
            combine = aggregate
            combine_kwargs = aggregate_kwargs

        chunk_kwargs = chunk_kwargs.copy() if chunk_kwargs else {}
        chunk_kwargs['aca_chunk'] = chunk

        combine_kwargs = combine_kwargs.copy() if combine_kwargs else {}
        combine_kwargs['aca_combine'] = combine

        aggregate_kwargs = aggregate_kwargs.copy() if aggregate_kwargs else {}
        aggregate_kwargs['aca_aggregate'] = aggregate

        return aca(self, chunk=_reduction_chunk, aggregate=_reduction_aggregate,
                   combine=_reduction_combine, meta=meta, token=token,
                   split_every=split_every, chunk_kwargs=chunk_kwargs,
                   aggregate_kwargs=aggregate_kwargs,
                   combine_kwargs=combine_kwargs, **kwargs)

    @derived_from(pd.DataFrame)
    def pipe(self, func, *args, **kwargs):
        # Taken from pandas:
        # https://github.com/pydata/pandas/blob/master/pandas/core/generic.py#L2698-L2707
        if isinstance(func, tuple):
            func, target = func
            if target in kwargs:
                raise ValueError('%s is both the pipe target and a keyword '
                                 'argument' % target)
            kwargs[target] = self
            return func(*args, **kwargs)
        else:
            return func(self, *args, **kwargs)

    def random_split(self, frac, random_state=None):
        """ Pseudorandomly split dataframe into different pieces row-wise

        Parameters
        ----------
        frac : list
            List of floats that should sum to one.
        random_state: int or np.random.RandomState
            If int create a new RandomState with this as the seed
        Otherwise draw from the passed RandomState

        Examples
        --------

        50/50 split

        >>> a, b = df.random_split([0.5, 0.5])  # doctest: +SKIP

        80/10/10 split, consistent random_state

        >>> a, b, c = df.random_split([0.8, 0.1, 0.1], random_state=123)  # doctest: +SKIP

        See Also
        --------
        dask.DataFrame.sample
        """
        if not np.allclose(sum(frac), 1):
            raise ValueError("frac should sum to 1")
        state_data = random_state_data(self.npartitions, random_state)
        token = tokenize(self, frac, random_state)
        name = 'split-' + token
        dsk = {(name, i): (pd_split, (self._name, i), frac, state)
               for i, state in enumerate(state_data)}

        out = []
        for i in range(len(frac)):
            name2 = 'split-%d-%s' % (i, token)
            dsk2 = {(name2, j): (getitem, (name, j), i)
                    for j in range(self.npartitions)}
            out.append(type(self)(merge(self.dask, dsk, dsk2), name2,
                                  self._meta, self.divisions))
        return out

    def head(self, n=5, npartitions=1, compute=True):
        """ First n rows of the dataset

        Parameters
        ----------
        n : int, optional
            The number of rows to return. Default is 5.
        npartitions : int, optional
            Elements are only taken from the first ``npartitions``, with a
            default of 1. If there are fewer than ``n`` rows in the first
            ``npartitions`` a warning will be raised and any found rows
            returned. Pass -1 to use all partitions.
        compute : bool, optional
            Whether to compute the result, default is True.
        """
        if npartitions <= -1:
            npartitions = self.npartitions
        if npartitions > self.npartitions:
            msg = "only {} partitions, head received {}"
            raise ValueError(msg.format(self.npartitions, npartitions))

        name = 'head-%d-%d-%s' % (npartitions, n, self._name)

        if npartitions > 1:
            name_p = 'head-partial-%d-%s' % (n, self._name)

            dsk = {}
            for i in range(npartitions):
                dsk[(name_p, i)] = (M.head, (self._name, i), n)

            concat = (_concat, [(name_p, i) for i in range(npartitions)])
            dsk[(name, 0)] = (safe_head, concat, n)
        else:
            dsk = {(name, 0): (safe_head, (self._name, 0), n)}

        result = new_dd_object(merge(self.dask, dsk), name, self._meta,
                               [self.divisions[0], self.divisions[npartitions]])

        if compute:
            result = result.compute()
        return result

    def tail(self, n=5, compute=True):
        """ Last n rows of the dataset

        Caveat, the only checks the last n rows of the last partition.
        """
        name = 'tail-%d-%s' % (n, self._name)
        dsk = {(name, 0): (M.tail, (self._name, self.npartitions - 1), n)}

        result = new_dd_object(merge(self.dask, dsk), name,
                               self._meta, self.divisions[-2:])

        if compute:
            result = result.compute()
        return result

    @property
    def loc(self):
        """ Purely label-location based indexer for selection by label.

        >>> df.loc["b"]  # doctest: +SKIP
        >>> df.loc["b":"d"]  # doctest: +SKIP"""
        from .indexing import _LocIndexer
        return _LocIndexer(self)

    # NOTE: `iloc` is not implemented because of performance concerns.
    # see https://github.com/dask/dask/pull/507

    def repartition(self, divisions=None, npartitions=None, freq=None, force=False):
        """ Repartition dataframe along new divisions

        Parameters
        ----------
        divisions : list, optional
            List of partitions to be used. If specified npartitions will be
            ignored.
        npartitions : int, optional
            Number of partitions of output. Only used if divisions isn't
            specified.
        freq : str, pd.Timedelta
            A period on which to partition timeseries data like ``'7D'`` or
            ``'12h'`` or ``pd.Timedelta(hours=12)``.  Assumes a datetime index.
        force : bool, default False
            Allows the expansion of the existing divisions.
            If False then the new divisions lower and upper bounds must be
            the same as the old divisions.

        Examples
        --------
        >>> df = df.repartition(npartitions=10)  # doctest: +SKIP
        >>> df = df.repartition(divisions=[0, 5, 10, 20])  # doctest: +SKIP
        >>> df = df.repartition(freq='7d')  # doctest: +SKIP
        """
        if npartitions is not None and divisions is not None:
            warnings.warn("When providing both npartitions and divisions to "
                          "repartition only npartitions is used.")

        if npartitions is not None:
            return repartition_npartitions(self, npartitions)
        elif divisions is not None:
            return repartition(self, divisions, force=force)
        elif freq is not None:
            return repartition_freq(self, freq=freq)
        else:
            raise ValueError(
                "Provide either divisions= or npartitions= to repartition")

    @derived_from(pd.DataFrame)
    def fillna(self, value=None, method=None, limit=None, axis=None):
        axis = self._validate_axis(axis)
        if method is None and limit is not None:
            raise NotImplementedError("fillna with set limit and method=None")
        if isinstance(value, _Frame):
            test_value = value._meta_nonempty.values[0]
        else:
            test_value = value
        meta = self._meta_nonempty.fillna(value=test_value, method=method,
                                          limit=limit, axis=axis)

        if axis == 1 or method is None:
            # Control whether or not dask's partition alignment happens.
            # We don't want for a pandas Series.
            # We do want it for a dask Series
            if isinstance(value, pd.Series):
                args = ()
                kwargs = {'value': value}
            else:
                args = (value,)
                kwargs = {}
            return self.map_partitions(M.fillna, *args, method=method,
                                       limit=limit, axis=axis, meta=meta,
                                       **kwargs)

        if method in ('pad', 'ffill'):
            method = 'ffill'
            skip_check = 0
            before, after = 1 if limit is None else limit, 0
        else:
            method = 'bfill'
            skip_check = self.npartitions - 1
            before, after = 0, 1 if limit is None else limit

        if limit is None:
            name = 'fillna-chunk-' + tokenize(self, method)
            dsk = {(name, i): (methods.fillna_check, (self._name, i),
                               method, i != skip_check)
                   for i in range(self.npartitions)}
            parts = new_dd_object(merge(dsk, self.dask), name, meta,
                                  self.divisions)
        else:
            parts = self

        return parts.map_overlap(M.fillna, before, after, method=method,
                                 limit=limit, meta=meta)

    @derived_from(pd.DataFrame)
    def ffill(self, axis=None, limit=None):
        return self.fillna(method='ffill', limit=limit, axis=axis)

    @derived_from(pd.DataFrame)
    def bfill(self, axis=None, limit=None):
        return self.fillna(method='bfill', limit=limit, axis=axis)

    def sample(self, n=None, frac=None, replace=False, random_state=None):
        """ Random sample of items

        Parameters
        ----------
        n : int, optional
            Number of items to return is not supported by dask. Use frac
            instead.
        frac : float, optional
            Fraction of axis items to return.
        replace : boolean, optional
            Sample with or without replacement. Default = False.
        random_state : int or ``np.random.RandomState``
            If int we create a new RandomState with this as the seed
            Otherwise we draw from the passed RandomState

        See Also
        --------
        DataFrame.random_split
        pandas.DataFrame.sample
        """
        if n is not None:
            msg = ("sample does not support the number of sampled items "
                   "parameter, 'n'. Please use the 'frac' parameter instead.")
            if isinstance(n, Number) and 0 <= n <= 1:
                warnings.warn(msg)
                frac = n
            else:
                raise ValueError(msg)

        if frac is None:
            raise ValueError("frac must not be None")

        if random_state is None:
            random_state = np.random.RandomState()

        name = 'sample-' + tokenize(self, frac, replace, random_state)

        state_data = random_state_data(self.npartitions, random_state)
        dsk = {(name, i): (methods.sample, (self._name, i), state, frac, replace)
               for i, state in enumerate(state_data)}

        return new_dd_object(merge(self.dask, dsk), name,
                             self._meta, self.divisions)

    def to_hdf(self, path_or_buf, key, mode='a', append=False, **kwargs):
        """ See dd.to_hdf docstring for more information """
        from .io import to_hdf
        return to_hdf(self, path_or_buf, key, mode, append, **kwargs)

    def to_parquet(self, path, *args, **kwargs):
        """ See dd.to_parquet docstring for more information """
        from .io import to_parquet
        return to_parquet(self, path, *args, **kwargs)

    def to_csv(self, filename, **kwargs):
        """ See dd.to_csv docstring for more information """
        from .io import to_csv
        return to_csv(self, filename, **kwargs)

    def to_json(self, filename, *args, **kwargs):
        """ See dd.to_json docstring for more information """
        from .io import to_json
        return to_json(self, filename, *args, **kwargs)

    def to_delayed(self, optimize_graph=True):
        """Convert into a list of ``dask.delayed`` objects, one per partition.

        Parameters
        ----------
        optimize_graph : bool, optional
            If True [default], the graph is optimized before converting into
            ``dask.delayed`` objects.

        Examples
        --------
        >>> partitions = df.to_delayed()  # doctest: +SKIP

        See Also
        --------
        dask.dataframe.from_delayed
        """
        from dask.delayed import Delayed
        keys = self.__dask_keys__()
        dsk = self.__dask_graph__()
        if optimize_graph:
            dsk = self.__dask_optimize__(dsk, keys)
        return [Delayed(k, dsk) for k in keys]

    @classmethod
    def _get_unary_operator(cls, op):
        return lambda self: elemwise(op, self)

    @classmethod
    def _get_binary_operator(cls, op, inv=False):
        if inv:
            return lambda self, other: elemwise(op, other, self)
        else:
            return lambda self, other: elemwise(op, self, other)

    def rolling(self, window, min_periods=None, freq=None, center=False,
                win_type=None, axis=0):
        """Provides rolling transformations.

        Parameters
        ----------
        window : int, str, offset
           Size of the moving window. This is the number of observations used
           for calculating the statistic. The window size must not be so large
           as to span more than one adjacent partition. If using an offset
           or offset alias like '5D', the data must have a ``DatetimeIndex``

           .. versionchanged:: 0.15.0

              Now accepts offsets and string offset aliases

        min_periods : int, default None
            Minimum number of observations in window required to have a value
            (otherwise result is NA).
        center : boolean, default False
            Set the labels at the center of the window.
        win_type : string, default None
            Provide a window type. The recognized window types are identical
            to pandas.
        axis : int, default 0

        Returns
        -------
        a Rolling object on which to call a method to compute a statistic

        Notes
        -----
        The `freq` argument is not supported.
        """
        from dask.dataframe.rolling import Rolling

        if isinstance(window, int):
            if window < 0:
                raise ValueError('window must be >= 0')

        if min_periods is not None:
            if not isinstance(min_periods, int):
                raise ValueError('min_periods must be an integer')
            if min_periods < 0:
                raise ValueError('min_periods must be >= 0')

        return Rolling(self, window=window, min_periods=min_periods,
                       freq=freq, center=center, win_type=win_type, axis=axis)

    @derived_from(pd.DataFrame)
    def diff(self, periods=1, axis=0):
        axis = self._validate_axis(axis)
        if not isinstance(periods, int):
            raise TypeError("periods must be an integer")

        if axis == 1:
            return self.map_partitions(M.diff, token='diff', periods=periods,
                                       axis=1)

        before, after = (periods, 0) if periods > 0 else (0, -periods)
        return self.map_overlap(M.diff, before, after, token='diff',
                                periods=periods)

    @derived_from(pd.DataFrame)
    def shift(self, periods=1, freq=None, axis=0):
        axis = self._validate_axis(axis)
        if not isinstance(periods, int):
            raise TypeError("periods must be an integer")

        if axis == 1:
            return self.map_partitions(M.shift, token='shift', periods=periods,
                                       freq=freq, axis=1)

        if freq is None:
            before, after = (periods, 0) if periods > 0 else (0, -periods)
            return self.map_overlap(M.shift, before, after, token='shift',
                                    periods=periods)

        # Let pandas error on invalid arguments
        meta = self._meta_nonempty.shift(periods, freq=freq)
        out = self.map_partitions(M.shift, token='shift', periods=periods,
                                  freq=freq, meta=meta)
        return maybe_shift_divisions(out, periods, freq=freq)

    def _reduction_agg(self, name, axis=None, skipna=True,
                       split_every=False, out=None):
        axis = self._validate_axis(axis)

        meta = getattr(self._meta_nonempty, name)(axis=axis, skipna=skipna)
        token = self._token_prefix + name

        method = getattr(M, name)
        if axis == 1:
            result = self.map_partitions(method, meta=meta,
                                         token=token, skipna=skipna, axis=axis)
            return handle_out(out, result)
        else:
            result = self.reduction(method, meta=meta, token=token,
                                    skipna=skipna, axis=axis,
                                    split_every=split_every)
            if isinstance(self, DataFrame):
                result.divisions = (min(self.columns), max(self.columns))
            return handle_out(out, result)

    @derived_from(pd.DataFrame)
    def abs(self):
        _raise_if_object_series(self, "abs")
        meta = self._meta_nonempty.abs()
        return self.map_partitions(M.abs, meta=meta)

    @derived_from(pd.DataFrame)
    def all(self, axis=None, skipna=True, split_every=False, out=None):
        return self._reduction_agg('all', axis=axis, skipna=skipna,
                                   split_every=split_every, out=out)

    @derived_from(pd.DataFrame)
    def any(self, axis=None, skipna=True, split_every=False, out=None):
        return self._reduction_agg('any', axis=axis, skipna=skipna,
                                   split_every=split_every, out=out)

    @derived_from(pd.DataFrame)
    def sum(self, axis=None, skipna=True, split_every=False, dtype=None, out=None):
        return self._reduction_agg('sum', axis=axis, skipna=skipna,
                                   split_every=split_every, out=out)

    @derived_from(pd.DataFrame)
    def prod(self, axis=None, skipna=True, split_every=False, dtype=None, out=None):
        return self._reduction_agg('prod', axis=axis, skipna=skipna,
                                   split_every=split_every, out=out)

    @derived_from(pd.DataFrame)
    def max(self, axis=None, skipna=True, split_every=False, out=None):
        return self._reduction_agg('max', axis=axis, skipna=skipna,
                                   split_every=split_every, out=out)

    @derived_from(pd.DataFrame)
    def min(self, axis=None, skipna=True, split_every=False, out=None):
        return self._reduction_agg('min', axis=axis, skipna=skipna,
                                   split_every=split_every, out=out)

    @derived_from(pd.DataFrame)
    def idxmax(self, axis=None, skipna=True, split_every=False):
        fn = 'idxmax'
        axis = self._validate_axis(axis)
        meta = self._meta_nonempty.idxmax(axis=axis, skipna=skipna)
        if axis == 1:
            return map_partitions(M.idxmax, self, meta=meta,
                                  token=self._token_prefix + fn,
                                  skipna=skipna, axis=axis)
        else:
            scalar = not isinstance(meta, pd.Series)
            result = aca([self], chunk=idxmaxmin_chunk, aggregate=idxmaxmin_agg,
                         combine=idxmaxmin_combine, meta=meta,
                         aggregate_kwargs={'scalar': scalar},
                         token=self._token_prefix + fn, split_every=split_every,
                         skipna=skipna, fn=fn)
            if isinstance(self, DataFrame):
                result.divisions = (min(self.columns), max(self.columns))
            return result

    @derived_from(pd.DataFrame)
    def idxmin(self, axis=None, skipna=True, split_every=False):
        fn = 'idxmin'
        axis = self._validate_axis(axis)
        meta = self._meta_nonempty.idxmax(axis=axis)
        if axis == 1:
            return map_partitions(M.idxmin, self, meta=meta,
                                  token=self._token_prefix + fn,
                                  skipna=skipna, axis=axis)
        else:
            scalar = not isinstance(meta, pd.Series)
            result = aca([self], chunk=idxmaxmin_chunk, aggregate=idxmaxmin_agg,
                         combine=idxmaxmin_combine, meta=meta,
                         aggregate_kwargs={'scalar': scalar},
                         token=self._token_prefix + fn, split_every=split_every,
                         skipna=skipna, fn=fn)
            if isinstance(self, DataFrame):
                result.divisions = (min(self.columns), max(self.columns))
            return result

    @derived_from(pd.DataFrame)
    def count(self, axis=None, split_every=False):
        axis = self._validate_axis(axis)
        token = self._token_prefix + 'count'
        if axis == 1:
            meta = self._meta_nonempty.count(axis=axis)
            return self.map_partitions(M.count, meta=meta, token=token,
                                       axis=axis)
        else:
            meta = self._meta_nonempty.count()
            result = self.reduction(M.count, aggregate=M.sum, meta=meta,
                                    token=token, split_every=split_every)
            if isinstance(self, DataFrame):
                result.divisions = (min(self.columns), max(self.columns))
            return result

    @derived_from(pd.DataFrame)
    def mean(self, axis=None, skipna=True, split_every=False, dtype=None, out=None):
        axis = self._validate_axis(axis)
        _raise_if_object_series(self, "mean")
        meta = self._meta_nonempty.mean(axis=axis, skipna=skipna)
        if axis == 1:
            result = map_partitions(M.mean, self, meta=meta,
                                    token=self._token_prefix + 'mean',
                                    axis=axis, skipna=skipna)
            return handle_out(out, result)
        else:
            num = self._get_numeric_data()
            s = num.sum(skipna=skipna, split_every=split_every)
            n = num.count(split_every=split_every)
            name = self._token_prefix + 'mean-%s' % tokenize(self, axis, skipna)
            result = map_partitions(methods.mean_aggregate, s, n,
                                    token=name, meta=meta)
            if isinstance(self, DataFrame):
                result.divisions = (min(self.columns), max(self.columns))
            return handle_out(out, result)

    @derived_from(pd.DataFrame)
    def var(self, axis=None, skipna=True, ddof=1, split_every=False, dtype=None, out=None):
        axis = self._validate_axis(axis)
        _raise_if_object_series(self, "var")
        meta = self._meta_nonempty.var(axis=axis, skipna=skipna)
        if axis == 1:
            result = map_partitions(M.var, self, meta=meta,
                                    token=self._token_prefix + 'var',
                                    axis=axis, skipna=skipna, ddof=ddof)
            return handle_out(out, result)
        else:
            num = self._get_numeric_data()
            x = 1.0 * num.sum(skipna=skipna, split_every=split_every)
            x2 = 1.0 * (num ** 2).sum(skipna=skipna, split_every=split_every)
            n = num.count(split_every=split_every)
            name = self._token_prefix + 'var'
            result = map_partitions(methods.var_aggregate, x2, x, n,
                                    token=name, meta=meta, ddof=ddof)
            if isinstance(self, DataFrame):
                result.divisions = (min(self.columns), max(self.columns))
            return handle_out(out, result)

    @derived_from(pd.DataFrame)
    def std(self, axis=None, skipna=True, ddof=1, split_every=False, dtype=None, out=None):
        axis = self._validate_axis(axis)
        _raise_if_object_series(self, "std")
        meta = self._meta_nonempty.std(axis=axis, skipna=skipna)
        if axis == 1:
            result = map_partitions(M.std, self, meta=meta,
                                    token=self._token_prefix + 'std',
                                    axis=axis, skipna=skipna, ddof=ddof)
            return handle_out(out, result)
        else:
            v = self.var(skipna=skipna, ddof=ddof, split_every=split_every)
            name = self._token_prefix + 'std'
            result = map_partitions(np.sqrt, v, meta=meta, token=name)
            return handle_out(out, result)

    @derived_from(pd.DataFrame)
    def sem(self, axis=None, skipna=None, ddof=1, split_every=False):
        axis = self._validate_axis(axis)
        _raise_if_object_series(self, "sem")
        meta = self._meta_nonempty.sem(axis=axis, skipna=skipna, ddof=ddof)
        if axis == 1:
            return map_partitions(M.sem, self, meta=meta,
                                  token=self._token_prefix + 'sem',
                                  axis=axis, skipna=skipna, ddof=ddof)
        else:
            num = self._get_numeric_data()
            v = num.var(skipna=skipna, ddof=ddof, split_every=split_every)
            n = num.count(split_every=split_every)
            name = self._token_prefix + 'sem'
            result = map_partitions(np.sqrt, v / n, meta=meta, token=name)
            if isinstance(self, DataFrame):
                result.divisions = (min(self.columns), max(self.columns))
            return result

    def quantile(self, q=0.5, axis=0):
        """ Approximate row-wise and precise column-wise quantiles of DataFrame

        Parameters
        ----------

        q : list/array of floats, default 0.5 (50%)
            Iterable of numbers ranging from 0 to 1 for the desired quantiles
        axis : {0, 1, 'index', 'columns'} (default 0)
            0 or 'index' for row-wise, 1 or 'columns' for column-wise
        """
        axis = self._validate_axis(axis)
        keyname = 'quantiles-concat--' + tokenize(self, q, axis)

        if axis == 1:
            if isinstance(q, list):
                # Not supported, the result will have current index as columns
                raise ValueError("'q' must be scalar when axis=1 is specified")
            return map_partitions(M.quantile, self, q, axis,
                                  token=keyname, meta=(q, 'f8'))
        else:
            _raise_if_object_series(self, "quantile")
            meta = self._meta.quantile(q, axis=axis)
            num = self._get_numeric_data()
            quantiles = tuple(quantile(self[c], q) for c in num.columns)

            dask = {}
            dask = merge(dask, *[_q.dask for _q in quantiles])
            qnames = [(_q._name, 0) for _q in quantiles]

            if isinstance(quantiles[0], Scalar):
                dask[(keyname, 0)] = (pd.Series, qnames, num.columns,
                                      None, meta.name)
                divisions = (min(num.columns), max(num.columns))
                return Series(dask, keyname, meta, divisions)
            else:
                dask[(keyname, 0)] = (methods.concat, qnames, 1)
                return DataFrame(dask, keyname, meta, quantiles[0].divisions)

    @derived_from(pd.DataFrame)
    def describe(self, split_every=False):
        # currently, only numeric describe is supported
        num = self._get_numeric_data()
        if self.ndim == 2 and len(num.columns) == 0:
            raise ValueError("DataFrame contains only non-numeric data.")
        elif self.ndim == 1 and self.dtype == 'object':
            raise ValueError("Cannot compute ``describe`` on object dtype.")

        stats = [num.count(split_every=split_every),
                 num.mean(split_every=split_every),
                 num.std(split_every=split_every),
                 num.min(split_every=split_every),
                 num.quantile([0.25, 0.5, 0.75]),
                 num.max(split_every=split_every)]
        stats_names = [(s._name, 0) for s in stats]

        name = 'describe--' + tokenize(self, split_every)
        dsk = merge(num.dask, *(s.dask for s in stats))
        dsk[(name, 0)] = (methods.describe_aggregate, stats_names)

        return new_dd_object(dsk, name, num._meta, divisions=[None, None])

    def _cum_agg(self, op_name, chunk, aggregate, axis, skipna=True,
                 chunk_kwargs=None, out=None):
        """ Wrapper for cumulative operation """

        axis = self._validate_axis(axis)

        if axis == 1:
            name = '{0}{1}(axis=1)'.format(self._token_prefix, op_name)
            result = self.map_partitions(chunk, token=name, **chunk_kwargs)
            return handle_out(out, result)
        else:
            # cumulate each partitions
            name1 = '{0}{1}-map'.format(self._token_prefix, op_name)
            cumpart = map_partitions(chunk, self, token=name1, meta=self,
                                     **chunk_kwargs)

            name2 = '{0}{1}-take-last'.format(self._token_prefix, op_name)
            cumlast = map_partitions(_take_last, cumpart, skipna,
                                     meta=pd.Series([]), token=name2)

            suffix = tokenize(self)
            name = '{0}{1}-{2}'.format(self._token_prefix, op_name, suffix)
            cname = '{0}{1}-cum-last-{2}'.format(self._token_prefix, op_name,
                                                 suffix)

            # aggregate cumulated partisions and its previous last element
            dask = {}
            dask[(name, 0)] = (cumpart._name, 0)

            for i in range(1, self.npartitions):
                # store each cumulative step to graph to reduce computation
                if i == 1:
                    dask[(cname, i)] = (cumlast._name, i - 1)
                else:
                    # aggregate with previous cumulation results
                    dask[(cname, i)] = (aggregate, (cname, i - 1),
                                        (cumlast._name, i - 1))
                dask[(name, i)] = (aggregate, (cumpart._name, i), (cname, i))
            result = new_dd_object(merge(dask, cumpart.dask, cumlast.dask),
                                   name, chunk(self._meta), self.divisions)
            return handle_out(out, result)

    @derived_from(pd.DataFrame)
    def cumsum(self, axis=None, skipna=True, dtype=None, out=None):
        return self._cum_agg('cumsum',
                             chunk=M.cumsum,
                             aggregate=operator.add,
                             axis=axis, skipna=skipna,
                             chunk_kwargs=dict(axis=axis, skipna=skipna),
                             out=out)

    @derived_from(pd.DataFrame)
    def cumprod(self, axis=None, skipna=True, dtype=None, out=None):
        return self._cum_agg('cumprod',
                             chunk=M.cumprod,
                             aggregate=operator.mul,
                             axis=axis, skipna=skipna,
                             chunk_kwargs=dict(axis=axis, skipna=skipna),
                             out=out)

    @derived_from(pd.DataFrame)
    def cummax(self, axis=None, skipna=True, out=None):
        return self._cum_agg('cummax',
                             chunk=M.cummax,
                             aggregate=methods.cummax_aggregate,
                             axis=axis, skipna=skipna,
                             chunk_kwargs=dict(axis=axis, skipna=skipna),
                             out=out)

    @derived_from(pd.DataFrame)
    def cummin(self, axis=None, skipna=True, out=None):
        return self._cum_agg('cummin',
                             chunk=M.cummin,
                             aggregate=methods.cummin_aggregate,
                             axis=axis, skipna=skipna,
                             chunk_kwargs=dict(axis=axis, skipna=skipna),
                             out=out)

    @derived_from(pd.DataFrame)
    def where(self, cond, other=np.nan):
        # cond and other may be dask instance,
        # passing map_partitions via keyword will not be aligned
        return map_partitions(M.where, self, cond, other)

    @derived_from(pd.DataFrame)
    def mask(self, cond, other=np.nan):
        return map_partitions(M.mask, self, cond, other)

    @derived_from(pd.DataFrame)
    def notnull(self):
        return self.map_partitions(M.notnull)

    @derived_from(pd.DataFrame)
    def isnull(self):
        return self.map_partitions(M.isnull)

    @derived_from(pd.DataFrame)
    def isna(self):
        if hasattr(pd, 'isna'):
            return self.map_partitions(M.isna)
        else:
            raise NotImplementedError("Need more recent version of Pandas "
                                      "to support isna. "
                                      "Please use isnull instead.")

    @derived_from(pd.DataFrame)
    def isin(self, values):
        return elemwise(M.isin, self, list(values))

    @derived_from(pd.DataFrame)
    def astype(self, dtype):
        # XXX: Pandas will segfault for empty dataframes when setting
        # categorical dtypes. This operation isn't allowed currently anyway. We
        # get the metadata with a non-empty frame to throw the error instead of
        # segfaulting.
        if isinstance(self._meta, pd.DataFrame) and is_categorical_dtype(dtype):
            meta = self._meta_nonempty.astype(dtype)
        else:
            meta = self._meta.astype(dtype)
        if hasattr(dtype, 'items'):
            # Pandas < 0.21.0, no `categories` attribute, so unknown
            # Pandas >= 0.21.0, known if `categories` attribute is not None
            set_unknown = [k for k, v in dtype.items()
                           if (is_categorical_dtype(v) and
                               getattr(v, 'categories', None) is None)]
            meta = clear_known_categories(meta, cols=set_unknown)
        elif (is_categorical_dtype(dtype) and
              getattr(dtype, 'categories', None) is None):
            meta = clear_known_categories(meta)
        return self.map_partitions(M.astype, dtype=dtype, meta=meta)

    @derived_from(pd.Series)
    def append(self, other):
        # because DataFrame.append will override the method,
        # wrap by pd.Series.append docstring
        from .multi import concat

        if isinstance(other, (list, dict)):
            msg = "append doesn't support list or dict input"
            raise NotImplementedError(msg)

        return concat([self, other], join='outer', interleave_partitions=False)

    @derived_from(pd.DataFrame)
    def align(self, other, join='outer', axis=None, fill_value=None):
        meta1, meta2 = _emulate(M.align, self, other, join, axis=axis,
                                fill_value=fill_value)
        aligned = self.map_partitions(M.align, other, join=join, axis=axis,
                                      fill_value=fill_value)

        token = tokenize(self, other, join, axis, fill_value)

        name1 = 'align1-' + token
        dsk1 = {(name1, i): (getitem, key, 0)
                for i, key in enumerate(aligned.__dask_keys__())}
        dsk1.update(aligned.dask)
        result1 = new_dd_object(dsk1, name1, meta1, aligned.divisions)

        name2 = 'align2-' + token
        dsk2 = {(name2, i): (getitem, key, 1)
                for i, key in enumerate(aligned.__dask_keys__())}
        dsk2.update(aligned.dask)
        result2 = new_dd_object(dsk2, name2, meta2, aligned.divisions)

        return result1, result2

    @derived_from(pd.DataFrame)
    def combine(self, other, func, fill_value=None, overwrite=True):
        return self.map_partitions(M.combine, other, func,
                                   fill_value=fill_value, overwrite=overwrite)

    @derived_from(pd.DataFrame)
    def combine_first(self, other):
        return self.map_partitions(M.combine_first, other)

    @classmethod
    def _bind_operator_method(cls, name, op):
        """ bind operator method like DataFrame.add to this class """
        raise NotImplementedError

    @derived_from(pd.DataFrame)
    def resample(self, rule, how=None, closed=None, label=None):
        from .tseries.resample import _resample
        return _resample(self, rule, how=how, closed=closed, label=label)

    @derived_from(pd.DataFrame)
    def first(self, offset):
        # Let pandas error on bad args
        self._meta_nonempty.first(offset)

        if not self.known_divisions:
            raise ValueError("`first` is not implemented for unknown divisions")

        offset = pd.tseries.frequencies.to_offset(offset)
        date = self.divisions[0] + offset
        end = self.loc._get_partitions(date)

        include_right = offset.isAnchored() or not hasattr(offset, '_inc')

        if end == self.npartitions - 1:
            divs = self.divisions
        else:
            divs = self.divisions[:end + 1] + (date,)

        name = 'first-' + tokenize(self, offset)
        dsk = {(name, i): (self._name, i) for i in range(end)}
        dsk[(name, end)] = (methods.boundary_slice, (self._name, end),
                            None, date, include_right, True, 'ix')
        return new_dd_object(merge(self.dask, dsk), name, self, divs)

    @derived_from(pd.DataFrame)
    def last(self, offset):
        # Let pandas error on bad args
        self._meta_nonempty.first(offset)

        if not self.known_divisions:
            raise ValueError("`last` is not implemented for unknown divisions")

        offset = pd.tseries.frequencies.to_offset(offset)
        date = self.divisions[-1] - offset
        start = self.loc._get_partitions(date)

        if start == 0:
            divs = self.divisions
        else:
            divs = (date,) + self.divisions[start + 1:]

        name = 'last-' + tokenize(self, offset)
        dsk = {(name, i + 1): (self._name, j + 1)
               for i, j in enumerate(range(start, self.npartitions))}
        dsk[(name, 0)] = (methods.boundary_slice, (self._name, start),
                          date, None, True, False, 'ix')
        return new_dd_object(merge(self.dask, dsk), name, self, divs)

    def nunique_approx(self, split_every=None):
        """Approximate number of unique rows.

        This method uses the HyperLogLog algorithm for cardinality
        estimation to compute the approximate number of unique rows.
        The approximate error is 0.406%.

        Parameters
        ----------
        split_every : int, optional
            Group partitions into groups of this size while performing a
            tree-reduction. If set to False, no tree-reduction will be used.
            Default is 8.

        Returns
        -------
        a float representing the approximate number of elements
        """
        from . import hyperloglog # here to avoid circular import issues

        return aca([self], chunk=hyperloglog.compute_hll_array,
                   combine=hyperloglog.reduce_state,
                   aggregate=hyperloglog.estimate_count,
                   split_every=split_every, b=16, meta=float)

    @property
    def values(self):
        """ Return a dask.array of the values of this dataframe

        Warning: This creates a dask.array without precise shape information.
        Operations that depend on shape information, like slicing or reshaping,
        will not work.
        """
        return self.map_partitions(methods.values)
