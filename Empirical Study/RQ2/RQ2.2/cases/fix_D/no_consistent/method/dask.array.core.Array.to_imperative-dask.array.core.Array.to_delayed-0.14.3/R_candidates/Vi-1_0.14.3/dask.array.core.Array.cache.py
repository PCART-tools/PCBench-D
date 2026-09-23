    def cache(self, store=None, **kwargs):
        """ Evaluate and cache array

        Parameters
        ----------
        store: MutableMapping or ndarray-like
            Place to put computed and cached chunks
        kwargs:
            Keyword arguments to pass on to ``get`` function for scheduling

        Examples
        --------

        This triggers evaluation and store the result in either

        1.  An ndarray object supporting setitem (see da.store)
        2.  A MutableMapping like a dict or chest

        It then returns a new dask array that points to this store.
        This returns a semantically equivalent dask array.

        >>> import dask.array as da
        >>> x = da.arange(5, chunks=2)
        >>> y = 2*x + 1
        >>> z = y.cache()  # triggers computation

        >>> y.compute()  # Does entire computation
        array([1, 3, 5, 7, 9])

        >>> z.compute()  # Just pulls from store
        array([1, 3, 5, 7, 9])

        You might base a cache off of an array like a numpy array or
        h5py.Dataset.

        >>> cache = np.empty(5, dtype=x.dtype)
        >>> z = y.cache(store=cache)
        >>> cache
        array([1, 3, 5, 7, 9])

        Or one might use a MutableMapping like a dict or chest

        >>> cache = dict()
        >>> z = y.cache(store=cache)
        >>> cache  # doctest: +SKIP
        {('x', 0): array([1, 3]),
         ('x', 1): array([5, 7]),
         ('x', 2): array([9])}
        """
        warnings.warn("Deprecation Warning: The `cache` method is deprecated, "
                      "and will be removed in the next release. To achieve "
                      "the same behavior, either write to disk or use "
                      "`Client.persist`, from `dask.distributed`.")
        if store is not None and hasattr(store, 'shape'):
            self.store(store)
            return from_array(store, chunks=self.chunks)
        if store is None:
            try:
                from chest import Chest
                store = Chest()
            except ImportError:
                if self.nbytes <= 1e9:
                    store = dict()
                else:
                    msg = ("No out-of-core storage found."
                           "Either:\n"
                           "1. Install ``chest``, an out-of-core dictionary\n"
                           "2. Provide an on-disk array like an h5py.Dataset")
                    raise ValueError(msg)   # pragma: no cover
        if isinstance(store, MutableMapping):
            name = 'cache-' + tokenize(self)
            dsk = dict(((name, k[1:]), (operator.setitem, store, (tuple, list(k)), k))
                       for k in core.flatten(self._keys()))
            Array._get(sharedict.merge(dsk, self.dask), list(dsk.keys()), **kwargs)

            dsk2 = dict((k, (operator.getitem, store, (tuple, list(k))))
                        for k in store)
            return Array(dsk2, self.name, chunks=self.chunks, dtype=self.dtype)
