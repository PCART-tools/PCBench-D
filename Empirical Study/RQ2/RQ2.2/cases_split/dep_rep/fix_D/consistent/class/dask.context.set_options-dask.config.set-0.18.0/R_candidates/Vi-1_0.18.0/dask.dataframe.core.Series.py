class Series(_Frame):
    """ Parallel Pandas Series

    Do not use this class directly.  Instead use functions like
    ``dd.read_csv``, ``dd.read_parquet``, or ``dd.from_pandas``.

    Parameters
    ----------

    dsk: dict
        The dask graph to compute this Series
    _name: str
        The key prefix that specifies which keys in the dask comprise this
        particular Series
    meta: pandas.Series
        An empty ``pandas.Series`` with names, dtypes, and index matching the
        expected output.
    divisions: tuple of index values
        Values along which we partition our blocks on the index

    See Also
    --------
    dask.dataframe.DataFrame
    """

    _partition_type = pd.Series
    _token_prefix = 'series-'

    def __array_wrap__(self, array, context=None):
        if isinstance(context, tuple) and len(context) > 0:
            if isinstance(context[1][0], np.ndarray) and context[1][0].shape == ():
                index = None
            else:
                index = context[1][0].index

        return pd.Series(array, index=index, name=self.name)

    @property
    def name(self):
        return self._meta.name

    @name.setter
    def name(self, name):
        self._meta.name = name
        renamed = _rename_dask(self, name)
        # update myself
        self.dask.update(renamed.dask)
        self._name = renamed._name

    @property
    def ndim(self):
        """ Return dimensionality """
        return 1

    @property
    def dtype(self):
        """ Return data type """
        return self._meta.dtype

    @cache_readonly
    def dt(self):
        """ Namespace of datetime methods """
        return DatetimeAccessor(self)

    @cache_readonly
    def cat(self):
        return CategoricalAccessor(self)

    @cache_readonly
    def str(self):
        """ Namespace for string methods """
        return StringAccessor(self)

    def __dir__(self):
        o = set(dir(type(self)))
        o.update(self.__dict__)
        # Remove the `cat` and `str` accessors if not available. We can't
        # decide this statically for the `dt` accessor, as it works on
        # datetime-like things as well.
        for accessor in ['cat', 'str']:
            if not hasattr(self._meta, accessor):
                o.remove(accessor)
        return list(o)

    @property
    def nbytes(self):
        """ Number of bytes """
        return self.reduction(methods.nbytes, np.sum, token='nbytes',
                              meta=int, split_every=False)

    @property
    def _repr_data(self):
        return _repr_data_series(self._meta, self._repr_divisions)

    def __repr__(self):
        """ have to overwrite footer """
        if self.name is not None:
            footer = "Name: {name}, dtype: {dtype}".format(name=self.name,
                                                           dtype=self.dtype)
        else:
            footer = "dtype: {dtype}".format(dtype=self.dtype)

        return """Dask {klass} Structure:
{data}
{footer}
Dask Name: {name}, {task} tasks""".format(klass=self.__class__.__name__,
                                          data=self.to_string(),
                                          footer=footer,
                                          name=key_split(self._name),
                                          task=len(self.dask))

    def rename(self, index=None, inplace=False, sorted_index=False):
        """Alter Series index labels or name

        Function / dict values must be unique (1-to-1). Labels not contained in
        a dict / Series will be left as-is. Extra labels listed don't throw an
        error.

        Alternatively, change ``Series.name`` with a scalar value.

        Parameters
        ----------
        index : scalar, hashable sequence, dict-like or callable, optional
            If dict-like or callable, the transformation is applied to the
            index. Scalar or hashable sequence-like will alter the
            ``Series.name`` attribute.
        inplace : boolean, default False
            Whether to return a new Series or modify this one inplace.
        sorted_index : bool, default False
            If true, the output ``Series`` will have known divisions inferred
            from the input series and the transformation. Ignored for
            non-callable/dict-like ``index`` or when the input series has
            unknown divisions. Note that this may only be set to ``True`` if
            you know that the transformed index is monotonicly increasing. Dask
            will check that transformed divisions are monotonic, but cannot
            check all the values between divisions, so incorrectly setting this
            can result in bugs.

        Returns
        -------
        renamed : Series

        See Also
        --------
        pandas.Series.rename
        """
        from pandas.api.types import is_scalar, is_list_like, is_dict_like
        if is_scalar(index) or (is_list_like(index) and not is_dict_like(index)):
            res = self if inplace else self.copy()
            res.name = index
        else:
            res = self.map_partitions(M.rename, index)
            if self.known_divisions:
                if sorted_index and (callable(index) or is_dict_like(index)):
                    old = pd.Series(range(self.npartitions + 1),
                                    index=self.divisions)
                    new = old.rename(index).index
                    if not new.is_monotonic_increasing:
                        msg = ("sorted_index=True, but the transformed index "
                               "isn't monotonic_increasing")
                        raise ValueError(msg)
                    res.divisions = tuple(new.tolist())
                else:
                    res = res.clear_divisions()
            if inplace:
                self.dask = res.dask
                self._name = res._name
                self.divisions = res.divisions
                self._meta = res._meta
                res = self
        return res

    @derived_from(pd.Series)
    def round(self, decimals=0):
        return elemwise(M.round, self, decimals)

    @derived_from(pd.DataFrame)
    def to_timestamp(self, freq=None, how='start', axis=0):
        df = elemwise(M.to_timestamp, self, freq, how, axis)
        df.divisions = tuple(pd.Index(self.divisions).to_timestamp())
        return df

    def quantile(self, q=0.5):
        """ Approximate quantiles of Series

        q : list/array of floats, default 0.5 (50%)
            Iterable of numbers ranging from 0 to 1 for the desired quantiles
        """
        return quantile(self, q)

    def _repartition_quantiles(self, npartitions, upsample=1.0):
        """ Approximate quantiles of Series used for repartitioning
        """
        from .partitionquantiles import partition_quantiles
        return partition_quantiles(self, npartitions, upsample=upsample)

    def __getitem__(self, key):
        if isinstance(key, Series) and self.divisions == key.divisions:
            name = 'index-%s' % tokenize(self, key)
            dsk = dict(((name, i), (operator.getitem, (self._name, i),
                                    (key._name, i)))
                       for i in range(self.npartitions))
            return Series(merge(self.dask, key.dask, dsk), name,
                          self._meta, self.divisions)
        raise NotImplementedError()

    @derived_from(pd.DataFrame)
    def _get_numeric_data(self, how='any', subset=None):
        return self

    @derived_from(pd.Series)
    def iteritems(self):
        for i in range(self.npartitions):
            s = self.get_partition(i).compute()
            for item in s.iteritems():
                yield item

    @classmethod
    def _validate_axis(cls, axis=0):
        if axis not in (0, 'index', None):
            raise ValueError('No axis named {0}'.format(axis))
        # convert to numeric axis
        return {None: 0, 'index': 0}.get(axis, axis)

    @derived_from(pd.Series)
    def groupby(self, by=None, **kwargs):
        from dask.dataframe.groupby import SeriesGroupBy
        return SeriesGroupBy(self, by=by, **kwargs)

    @derived_from(pd.Series)
    def count(self, split_every=False):
        return super(Series, self).count(split_every=split_every)

    def unique(self, split_every=None, split_out=1):
        """
        Return Series of unique values in the object. Includes NA values.

        Returns
        -------
        uniques : Series
        """
        return aca(self, chunk=methods.unique, aggregate=methods.unique,
                   meta=self._meta, token='unique', split_every=split_every,
                   series_name=self.name, split_out=split_out)

    @derived_from(pd.Series)
    def nunique(self, split_every=None):
        return self.drop_duplicates(split_every=split_every).count()

    @derived_from(pd.Series)
    def value_counts(self, split_every=None, split_out=1):
        return aca(self, chunk=M.value_counts,
                   aggregate=methods.value_counts_aggregate,
                   combine=methods.value_counts_combine,
                   meta=self._meta.value_counts(), token='value-counts',
                   split_every=split_every, split_out=split_out,
                   split_out_setup=split_out_on_index)

    @derived_from(pd.Series)
    def nlargest(self, n=5, split_every=None):
        return aca(self, chunk=M.nlargest, aggregate=M.nlargest,
                   meta=self._meta, token='series-nlargest',
                   split_every=split_every, n=n)

    @derived_from(pd.Series)
    def nsmallest(self, n=5, split_every=None):
        return aca(self, chunk=M.nsmallest, aggregate=M.nsmallest,
                   meta=self._meta, token='series-nsmallest',
                   split_every=split_every, n=n)

    @derived_from(pd.Series)
    def isin(self, values):
        return elemwise(M.isin, self, list(values))

    @insert_meta_param_description(pad=12)
    @derived_from(pd.Series)
    def map(self, arg, na_action=None, meta=no_default):
        if not (isinstance(arg, (pd.Series, dict)) or callable(arg)):
            raise TypeError("arg must be pandas.Series, dict or callable."
                            " Got {0}".format(type(arg)))
        name = 'map-' + tokenize(self, arg, na_action)
        dsk = {(name, i): (M.map, k, arg, na_action) for i, k in
               enumerate(self.__dask_keys__())}
        dsk.update(self.dask)
        if meta is no_default:
            meta = _emulate(M.map, self, arg, na_action=na_action, udf=True)
        else:
            meta = make_meta(meta)

        return Series(dsk, name, meta, self.divisions)

    @derived_from(pd.Series)
    def dropna(self):
        return self.map_partitions(M.dropna)

    @derived_from(pd.Series)
    def between(self, left, right, inclusive=True):
        return self.map_partitions(M.between, left=left,
                                   right=right, inclusive=inclusive)

    @derived_from(pd.Series)
    def clip(self, lower=None, upper=None, out=None):
        if out is not None:
            raise ValueError("'out' must be None")
        # np.clip may pass out
        return self.map_partitions(M.clip, lower=lower, upper=upper)

    @derived_from(pd.Series)
    def clip_lower(self, threshold):
        return self.map_partitions(M.clip_lower, threshold=threshold)

    @derived_from(pd.Series)
    def clip_upper(self, threshold):
        return self.map_partitions(M.clip_upper, threshold=threshold)

    @derived_from(pd.Series)
    def align(self, other, join='outer', axis=None, fill_value=None):
        return super(Series, self).align(other, join=join, axis=axis,
                                         fill_value=fill_value)

    @derived_from(pd.Series)
    def combine(self, other, func, fill_value=None):
        return self.map_partitions(M.combine, other, func,
                                   fill_value=fill_value)

    @derived_from(pd.Series)
    def squeeze(self):
        return self

    @derived_from(pd.Series)
    def combine_first(self, other):
        return self.map_partitions(M.combine_first, other)

    def to_bag(self, index=False):
        """ Craeate a Dask Bag from a Series """
        from .io import to_bag
        return to_bag(self, index)

    @derived_from(pd.Series)
    def to_frame(self, name=None):
        return self.map_partitions(M.to_frame, name,
                                   meta=self._meta.to_frame(name))

    @derived_from(pd.Series)
    def to_string(self, max_rows=5):
        # option_context doesn't affect
        return self._repr_data.to_string(max_rows=max_rows)

    @classmethod
    def _bind_operator_method(cls, name, op):
        """ bind operator method like DataFrame.add to this class """

        def meth(self, other, level=None, fill_value=None, axis=0):
            if level is not None:
                raise NotImplementedError('level must be None')
            axis = self._validate_axis(axis)
            meta = _emulate(op, self, other, axis=axis, fill_value=fill_value)
            return map_partitions(op, self, other, meta=meta,
                                  axis=axis, fill_value=fill_value)
        meth.__doc__ = op.__doc__
        bind_method(cls, name, meth)

    @classmethod
    def _bind_comparison_method(cls, name, comparison):
        """ bind comparison method like DataFrame.add to this class """

        def meth(self, other, level=None, axis=0):
            if level is not None:
                raise NotImplementedError('level must be None')
            axis = self._validate_axis(axis)
            return elemwise(comparison, self, other, axis=axis)

        meth.__doc__ = comparison.__doc__
        bind_method(cls, name, meth)

    @insert_meta_param_description(pad=12)
    def apply(self, func, convert_dtype=True, meta=no_default, args=(), **kwds):
        """ Parallel version of pandas.Series.apply

        Parameters
        ----------
        func : function
            Function to apply
        convert_dtype : boolean, default True
            Try to find better dtype for elementwise function results.
            If False, leave as dtype=object.
        $META
        args : tuple
            Positional arguments to pass to function in addition to the value.

        Additional keyword arguments will be passed as keywords to the function.

        Returns
        -------
        applied : Series or DataFrame if func returns a Series.

        Examples
        --------
        >>> import dask.dataframe as dd
        >>> s = pd.Series(range(5), name='x')
        >>> ds = dd.from_pandas(s, npartitions=2)

        Apply a function elementwise across the Series, passing in extra
        arguments in ``args`` and ``kwargs``:

        >>> def myadd(x, a, b=1):
        ...     return x + a + b
        >>> res = ds.apply(myadd, args=(2,), b=1.5)

        By default, dask tries to infer the output metadata by running your
        provided function on some fake data. This works well in many cases, but
        can sometimes be expensive, or even fail. To avoid this, you can
        manually specify the output metadata with the ``meta`` keyword. This
        can be specified in many forms, for more information see
        ``dask.dataframe.utils.make_meta``.

        Here we specify the output is a Series with name ``'x'``, and dtype
        ``float64``:

        >>> res = ds.apply(myadd, args=(2,), b=1.5, meta=('x', 'f8'))

        In the case where the metadata doesn't change, you can also pass in
        the object itself directly:

        >>> res = ds.apply(lambda x: x + 1, meta=ds)

        See Also
        --------
        dask.Series.map_partitions
        """
        if meta is no_default:
            msg = ("`meta` is not specified, inferred from partial data. "
                   "Please provide `meta` if the result is unexpected.\n"
                   "  Before: .apply(func)\n"
                   "  After:  .apply(func, meta={'x': 'f8', 'y': 'f8'}) for dataframe result\n"
                   "  or:     .apply(func, meta=('x', 'f8'))            for series result")
            warnings.warn(msg)

            meta = _emulate(M.apply, self._meta_nonempty, func,
                            convert_dtype=convert_dtype,
                            args=args, udf=True, **kwds)

        return map_partitions(M.apply, self, func,
                              convert_dtype, args, meta=meta, **kwds)

    @derived_from(pd.Series)
    def cov(self, other, min_periods=None, split_every=False):
        from .multi import concat
        if not isinstance(other, Series):
            raise TypeError("other must be a dask.dataframe.Series")
        df = concat([self, other], axis=1)
        return cov_corr(df, min_periods, scalar=True, split_every=split_every)

    @derived_from(pd.Series)
    def corr(self, other, method='pearson', min_periods=None,
             split_every=False):
        from .multi import concat
        if not isinstance(other, Series):
            raise TypeError("other must be a dask.dataframe.Series")
        if method != 'pearson':
            raise NotImplementedError("Only Pearson correlation has been "
                                      "implemented")
        df = concat([self, other], axis=1)
        return cov_corr(df, min_periods, corr=True, scalar=True,
                        split_every=split_every)

    @derived_from(pd.Series)
    def autocorr(self, lag=1, split_every=False):
        if not isinstance(lag, int):
            raise TypeError("lag must be an integer")
        return self.corr(self if lag == 0 else self.shift(lag),
                         split_every=split_every)

    @derived_from(pd.Series)
    def memory_usage(self, index=True, deep=False):
        from ..delayed import delayed
        result = self.map_partitions(M.memory_usage, index=index, deep=deep)
        return delayed(sum)(result.to_delayed())
