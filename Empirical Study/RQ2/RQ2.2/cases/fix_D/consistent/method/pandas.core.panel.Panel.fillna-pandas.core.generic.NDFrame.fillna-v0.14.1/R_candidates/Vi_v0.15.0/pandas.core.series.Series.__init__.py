    def __init__(self, data=None, index=None, dtype=None, name=None,
                 copy=False, fastpath=False):

        # we are called internally, so short-circuit
        if fastpath:

            # data is an ndarray, index is defined
            if not isinstance(data, SingleBlockManager):
                data = SingleBlockManager(data, index, fastpath=True)
            if copy:
                data = data.copy()
            if index is None:
                index = data.index

        else:

            if index is not None:
                index = _ensure_index(index)

            if data is None:
                data = {}
            if dtype is not None:
                dtype = self._validate_dtype(dtype)

            if isinstance(data, MultiIndex):
                raise NotImplementedError
            elif isinstance(data, Index):
                # need to copy to avoid aliasing issues
                if name is None:
                    name = data.name

                data = data._to_embed(keep_tz=True)
                copy = True
            elif isinstance(data, np.ndarray):
                pass
            elif isinstance(data, Series):
                if name is None:
                    name = data.name
                if index is None:
                    index = data.index
                else:
                    data = data.reindex(index, copy=copy)
                data = data._data
            elif isinstance(data, dict):
                if index is None:
                    if isinstance(data, OrderedDict):
                        index = Index(data)
                    else:
                        index = Index(_try_sort(data))
                try:
                    if isinstance(index, DatetimeIndex):
                        # coerce back to datetime objects for lookup
                        data = lib.fast_multiget(data, index.astype('O'),
                                                 default=np.nan)
                    elif isinstance(index, PeriodIndex):
                        data = [data.get(i, nan) for i in index]
                    else:
                        data = lib.fast_multiget(data, index.values,
                                                 default=np.nan)
                except TypeError:
                    data = [data.get(i, nan) for i in index]

            elif isinstance(data, SingleBlockManager):
                if index is None:
                    index = data.index
                else:
                    data = data.reindex(index, copy=copy)
            elif isinstance(data, Categorical):
                if dtype is not None:
                    raise ValueError("cannot specify a dtype with a Categorical")
                if name is None:
                    name = data.name
            elif isinstance(data, types.GeneratorType):
                data = list(data)
            elif isinstance(data, (set, frozenset)):
                raise TypeError("{0!r} type is unordered"
                                "".format(data.__class__.__name__))
            else:

                # handle sparse passed here (and force conversion)
                if isinstance(data, ABCSparseArray):
                    data = data.to_dense()

            if index is None:
                if not is_list_like(data):
                    data = [data]
                index = _default_index(len(data))

            # create/copy the manager
            if isinstance(data, SingleBlockManager):
                if dtype is not None:
                    data = data.astype(dtype=dtype, raise_on_error=False)
                elif copy:
                    data = data.copy()
            else:
                data = _sanitize_array(data, index, dtype, copy,
                                       raise_cast_failure=True)

                data = SingleBlockManager(data, index, fastpath=True)

        generic.NDFrame.__init__(self, data, fastpath=True)

        object.__setattr__(self, 'name', name)
        self._set_axis(0, index, fastpath=True)
