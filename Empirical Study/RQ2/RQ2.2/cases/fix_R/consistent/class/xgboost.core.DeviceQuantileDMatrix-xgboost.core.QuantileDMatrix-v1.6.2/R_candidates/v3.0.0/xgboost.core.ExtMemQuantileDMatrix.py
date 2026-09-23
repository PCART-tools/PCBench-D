class ExtMemQuantileDMatrix(DMatrix, _RefMixIn):
    """The external memory version of the :py:class:`QuantileDMatrix`.

    See :doc:`/tutorials/external_memory` for explanation and usage examples, and
    :py:class:`QuantileDMatrix` for parameter document.

    .. warning::

        This is an experimental feature and subject to change.

    .. versionadded:: 3.0.0

    """

    @_deprecate_positional_args
    def __init__(  # pylint: disable=super-init-not-called
        self,
        data: DataIter,
        *,
        missing: Optional[float] = None,
        nthread: Optional[int] = None,
        max_bin: Optional[int] = None,
        ref: Optional[DMatrix] = None,
        enable_categorical: bool = False,
        max_num_device_pages: Optional[int] = None,
        max_quantile_batches: Optional[int] = None,
    ) -> None:
        """
        Parameters
        ----------
        data :
            A user-defined :py:class:`DataIter` for loading data.

        max_num_device_pages :
            For a GPU-based validation dataset, XGBoost can optionally cache some pages
            in device memory instead of host memory to reduce data transfer. Each cached
            page has size of `min_cache_page_bytes`. Set this to 0 if you don't want
            pages to be cached in the device memory. This can be useful for preventing
            OOM error where there are more than one validation datasets. The default
            number of device-based page is 1. Lastly, XGBoost infers whether a dataset
            is used for valdiation by checking whether ref is not None.

        max_quantile_batches :
            See :py:class:`QuantileDMatrix`.

        """
        self.max_bin = max_bin
        self.missing = missing if missing is not None else np.nan
        self.nthread = nthread if nthread is not None else -1

        self._init(
            data,
            ref,
            enable_categorical=enable_categorical,
            max_num_device_pages=max_num_device_pages,
            max_quantile_blocks=max_quantile_batches,
        )
        assert self.handle is not None

    def _init(
        self,
        it: DataIter,
        ref: Optional[DMatrix],
        *,
        enable_categorical: bool,
        max_num_device_pages: Optional[int] = None,
        max_quantile_blocks: Optional[int] = None,
    ) -> None:
        args = make_jcargs(
            missing=self.missing,
            nthread=self.nthread,
            cache_prefix=it.cache_prefix if it.cache_prefix else "",
            on_host=it.on_host,
            max_bin=self.max_bin,
            min_cache_page_bytes=it.min_cache_page_bytes,
            max_num_device_pages=max_num_device_pages,
            # It's called blocks internally due to block-based quantile sketching.
            max_quantile_blocks=max_quantile_blocks,
        )
        handle = ctypes.c_void_p()
        reset_callback, next_callback = it.get_callbacks(enable_categorical)
        # We don't need the iter handle (hence None) in Python as reset,next callbacks
        # are member functions, and ctypes can handle the `self` parameter
        # automatically.
        ret = _LIB.XGExtMemQuantileDMatrixCreateFromCallback(
            None,  # iter
            it.proxy.handle,  # proxy
            ref.handle if ref is not None else ref,  # ref
            reset_callback,  # reset
            next_callback,  # next
            args,  # config
            ctypes.byref(handle),  # out
        )
        it.reraise()
        # delay check_call to throw intermediate exception first
        _check_call(ret)
        self.handle = handle

        if ref is not None:
            self.ref = weakref.ref(ref)
