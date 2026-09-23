    def __init__(
        self,
        data=None,
        index=None,
        dtype: Dtype | None = None,
        name=None,
        copy: bool = False,
        fastpath: bool = False,
    ):

        if (
            isinstance(data, (SingleBlockManager, SingleArrayManager))
            and index is None
            and dtype is None
            and copy is False
        ):
            # GH#33357 called with just the SingleBlockManager
            NDFrame.__init__(self, data)
            if fastpath:
                # e.g. from _box_col_values, skip validation of name
                object.__setattr__(self, "_name", name)
            else:
                self.name = name
            return

        # we are called internally, so short-circuit
        if fastpath:

            # data is an ndarray, index is defined
            if not isinstance(data, (SingleBlockManager, SingleArrayManager)):
                manager = get_option("mode.data_manager")
                if manager == "block":
                    data = SingleBlockManager.from_array(data, index)
                elif manager == "array":
                    data = SingleArrayManager.from_array(data, index)
            if copy:
                data = data.copy()
            if index is None:
                index = data.index

        else:

            name = ibase.maybe_extract_name(name, data, type(self))

            if is_empty_data(data) and dtype is None:
                # gh-17261
                warnings.warn(
                    "The default dtype for empty Series will be 'object' instead "
                    "of 'float64' in a future version. Specify a dtype explicitly "
                    "to silence this warning.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
                # uncomment the line below when removing the FutureWarning
                # dtype = np.dtype(object)

            if index is not None:
                index = ensure_index(index)

            if data is None:
                data = {}
            if dtype is not None:
                dtype = self._validate_dtype(dtype)

            if isinstance(data, MultiIndex):
                raise NotImplementedError(
                    "initializing a Series from a MultiIndex is not supported"
                )
            elif isinstance(data, Index):

                if dtype is not None:
                    # astype copies
                    data = data.astype(dtype)
                else:
                    # GH#24096 we need to ensure the index remains immutable
                    data = data._values.copy()
                copy = False

            elif isinstance(data, np.ndarray):
                if len(data.dtype):
                    # GH#13296 we are dealing with a compound dtype, which
                    #  should be treated as 2D
                    raise ValueError(
                        "Cannot construct a Series from an ndarray with "
                        "compound dtype.  Use DataFrame instead."
                    )
            elif isinstance(data, Series):
                if index is None:
                    index = data.index
                else:
                    data = data.reindex(index, copy=copy)
                    copy = False
                data = data._mgr
            elif is_dict_like(data):
                data, index = self._init_dict(data, index, dtype)
                dtype = None
                copy = False
            elif isinstance(data, (SingleBlockManager, SingleArrayManager)):
                if index is None:
                    index = data.index
                elif not data.index.equals(index) or copy:
                    # GH#19275 SingleBlockManager input should only be called
                    # internally
                    raise AssertionError(
                        "Cannot pass both SingleBlockManager "
                        "`data` argument and a different "
                        "`index` argument. `copy` must be False."
                    )

            elif isinstance(data, ExtensionArray):
                pass
            else:
                data = com.maybe_iterable_to_list(data)

            if index is None:
                if not is_list_like(data):
                    data = [data]
                index = default_index(len(data))
            elif is_list_like(data):
                com.require_length_match(data, index)

            # create/copy the manager
            if isinstance(data, (SingleBlockManager, SingleArrayManager)):
                if dtype is not None:
                    data = data.astype(dtype=dtype, errors="ignore", copy=copy)
                elif copy:
                    data = data.copy()
            else:
                data = sanitize_array(data, index, dtype, copy)

                manager = get_option("mode.data_manager")
                if manager == "block":
                    data = SingleBlockManager.from_array(data, index)
                elif manager == "array":
                    data = SingleArrayManager.from_array(data, index)

        NDFrame.__init__(self, data)
        self.name = name
        self._set_axis(0, index, fastpath=True)
