    def __init__(
        self, data=None, index=None, dtype=None, name=None, copy=False, fastpath=False
    ):

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
                index = ensure_index(index)

            if data is None:
                data = {}
            if dtype is not None:
                # GH 26336: explicitly handle 'category' to avoid warning
                # TODO: Remove after CategoricalDtype defaults to ordered=False
                if (
                    isinstance(dtype, str)
                    and dtype == "category"
                    and is_categorical(data)
                ):
                    dtype = data.dtype

                dtype = self._validate_dtype(dtype)

            if isinstance(data, MultiIndex):
                raise NotImplementedError(
                    "initializing a Series from a " "MultiIndex is not supported"
                )
            elif isinstance(data, Index):
                if name is None:
                    name = data.name

                if dtype is not None:
                    # astype copies
                    data = data.astype(dtype)
                else:
                    # need to copy to avoid aliasing issues
                    data = data._values.copy()
                    if isinstance(data, ABCDatetimeIndex) and data.tz is not None:
                        # GH#24096 need copy to be deep for datetime64tz case
                        # TODO: See if we can avoid these copies
                        data = data._values.copy(deep=True)
                copy = False

            elif isinstance(data, np.ndarray):
                pass
            elif isinstance(data, (ABCSeries, ABCSparseSeries)):
                if name is None:
                    name = data.name
                if index is None:
                    index = data.index
                else:
                    data = data.reindex(index, copy=copy)
                data = data._data
            elif isinstance(data, dict):
                data, index = self._init_dict(data, index, dtype)
                dtype = None
                copy = False
            elif isinstance(data, SingleBlockManager):
                if index is None:
                    index = data.index
                elif not data.index.equals(index) or copy:
                    # GH#19275 SingleBlockManager input should only be called
                    # internally
                    raise AssertionError(
                        "Cannot pass both SingleBlockManager "
                        "`data` argument and a different "
                        "`index` argument.  `copy` must "
                        "be False."
                    )

            elif is_extension_array_dtype(data):
                pass
            elif isinstance(data, (set, frozenset)):
                raise TypeError(
                    "{0!r} type is unordered" "".format(data.__class__.__name__)
                )
            elif isinstance(data, ABCSparseArray):
                # handle sparse passed here (and force conversion)
                data = data.to_dense()
            else:
                data = com.maybe_iterable_to_list(data)

            if index is None:
                if not is_list_like(data):
                    data = [data]
                index = ibase.default_index(len(data))
            elif is_list_like(data):

                # a scalar numpy array is list-like but doesn't
                # have a proper length
                try:
                    if len(index) != len(data):
                        raise ValueError(
                            "Length of passed values is {val}, "
                            "index implies {ind}".format(val=len(data), ind=len(index))
                        )
                except TypeError:
                    pass

            # create/copy the manager
            if isinstance(data, SingleBlockManager):
                if dtype is not None:
                    data = data.astype(dtype=dtype, errors="ignore", copy=copy)
                elif copy:
                    data = data.copy()
            else:
                data = sanitize_array(data, index, dtype, copy, raise_cast_failure=True)

                data = SingleBlockManager(data, index, fastpath=True)

        generic.NDFrame.__init__(self, data, fastpath=True)

        self.name = name
        self._set_axis(0, index, fastpath=True)
