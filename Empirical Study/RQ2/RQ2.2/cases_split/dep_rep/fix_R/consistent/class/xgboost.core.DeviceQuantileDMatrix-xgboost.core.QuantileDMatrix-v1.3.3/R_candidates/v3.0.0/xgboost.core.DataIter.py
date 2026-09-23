class DataIter(ABC):  # pylint: disable=too-many-instance-attributes
    """The interface for user defined data iterator. The iterator facilitates
    distributed training, :py:class:`QuantileDMatrix`, and external memory support using
    :py:class:`DMatrix` or :py:class:`ExtMemQuantileDMatrix`. Most of time, users don't
    need to interact with this class directly.

    .. note::

        The class caches some intermediate results using the `data` input (predictor
        `X`) as key. Don't repeat the `X` for multiple batches with different meta data
        (like `label`), make a copy if necessary.

    Parameters
    ----------
    cache_prefix :
        Prefix to the cache files, only used in external memory.

        Note that using this class for external memory **will cache data
        on disk** under the path passed here.

    release_data :
        Whether the iterator should release the data during iteration. Set it to True if
        the data transformation (converting data to np.float32 type) is memory
        intensive. Otherwise, if the transformation is computation intensive then we can
        keep the cache.

    on_host :
        Whether the data should be cached on the host memory instead of the file system
        when using GPU with external memory. When set to true (the default), the
        "external memory" is the CPU (host) memory. See
        :doc:`/tutorials/external_memory` for more info.

        .. versionadded:: 3.0.0

        .. warning::

            This is an experimental parameter and subject to change.

    min_cache_page_bytes :
        The minimum number of bytes of each cached pages. Only used for on-host cache
        with GPU-based :py:class:`ExtMemQuantileDMatrix`. When using GPU-based external
        memory with the data cached in the host memory, XGBoost can concatenate the
        pages internally to increase the batch size for the GPU. The default page size
        is about 1/8 of the total device memory. Users can manually set the value based
        on the actual hardware and datasets. Set this to 0 to disable page
        concatenation.

        .. versionadded:: 3.0.0

        .. warning::

            This is an experimental parameter and subject to change.

    """

    def __init__(
        self,
        cache_prefix: Optional[str] = None,
        release_data: bool = True,
        *,
        on_host: bool = True,
        min_cache_page_bytes: Optional[int] = None,
    ) -> None:
        self.cache_prefix = cache_prefix
        self.on_host = on_host
        self.min_cache_page_bytes = min_cache_page_bytes

        self._handle = _ProxyDMatrix()
        self._exception: Optional[Exception] = None
        self._enable_categorical = False
        self._release = release_data
        # Stage data in Python until reset or next is called to avoid data being free.
        self._temporary_data: Optional[TransformedData] = None
        self._data_ref: Optional[weakref.ReferenceType] = None

    def get_callbacks(self, enable_categorical: bool) -> Tuple[Callable, Callable]:
        """Get callback functions for iterating in C. This is an internal function."""
        assert hasattr(self, "cache_prefix"), "__init__ is not called."
        reset_callback = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(self._reset_wrapper)
        next_callback = ctypes.CFUNCTYPE(
            ctypes.c_int,
            ctypes.c_void_p,
        )(self._next_wrapper)
        self._enable_categorical = enable_categorical
        return reset_callback, next_callback

    @property
    def proxy(self) -> "_ProxyDMatrix":
        """Handle of DMatrix proxy."""
        return self._handle

    def _handle_exception(self, fn: Callable, dft_ret: _T) -> _T:
        if self._exception is not None:
            return dft_ret

        try:
            return fn()
        except Exception as e:  # pylint: disable=broad-except
            # Defer the exception in order to return 0 and stop the iteration.
            # Exception inside a ctype callback function has no effect except
            # for printing to stderr (doesn't stop the execution).
            tb = sys.exc_info()[2]
            # On dask, the worker is restarted and somehow the information is
            # lost.
            self._exception = e.with_traceback(tb)
        return dft_ret

    def reraise(self) -> None:
        """Reraise the exception thrown during iteration."""
        self._temporary_data = None
        if self._exception is not None:
            #  pylint 2.7.0 believes `self._exception` can be None even with `assert
            #  isinstace`
            exc = self._exception
            self._exception = None
            raise exc  # pylint: disable=raising-bad-type

    def __del__(self) -> None:
        assert self._temporary_data is None
        assert self._exception is None

    def _reset_wrapper(self, this: None) -> None:  # pylint: disable=unused-argument
        """A wrapper for user defined `reset` function."""
        # free the data
        if self._release:
            self._temporary_data = None
        self._handle_exception(self.reset, None)

    def _next_wrapper(self, this: None) -> int:  # pylint: disable=unused-argument
        """A wrapper for user defined `next` function.

        `this` is not used in Python.  ctypes can handle `self` of a Python
        member function automatically when converting it to c function
        pointer.

        """

        @require_keyword_args(True)
        def input_data(
            *,
            data: Any,
            feature_names: Optional[FeatureNames] = None,
            feature_types: Optional[FeatureTypes] = None,
            **kwargs: Any,
        ) -> None:
            from .data import _proxy_transform, dispatch_proxy_set_data

            # Reduce the amount of transformation that's needed for QuantileDMatrix.
            #
            # To construct the QDM, one needs 4 iterations on CPU, or 2 iterations on
            # GPU. If the QDM has only one batch of input (most of the cases), we can
            # avoid transforming the data repeatly.
            try:
                ref = weakref.ref(data)
            except TypeError:
                ref = None
            if (
                self._temporary_data is not None
                and ref is not None
                and ref is self._data_ref
            ):
                new, cat_codes, feature_names, feature_types = self._temporary_data
            else:
                new, cat_codes, feature_names, feature_types = _proxy_transform(
                    data,
                    feature_names,
                    feature_types,
                    self._enable_categorical,
                )
            # Stage the data, meta info are copied inside C++ MetaInfo.
            self._temporary_data = (new, cat_codes, feature_names, feature_types)
            dispatch_proxy_set_data(self.proxy, new, cat_codes)
            self.proxy.set_info(
                feature_names=feature_names,
                feature_types=feature_types,
                **kwargs,
            )
            self._data_ref = ref

        # Release the data before next batch is loaded.
        if self._release:
            self._temporary_data = None
        # pylint: disable=not-callable
        return self._handle_exception(lambda: int(self.next(input_data)), 0)

    @abstractmethod
    def reset(self) -> None:
        """Reset the data iterator.  Prototype for user defined function."""
        raise NotImplementedError()

    @abstractmethod
    def next(self, input_data: Callable) -> bool:
        """Set the next batch of data.

        Parameters
        ----------

        input_data:
            A function with same data fields like `data`, `label` with
            `xgboost.DMatrix`.

        Returns
        -------
        False if there's no more batch, otherwise True.

        """
        raise NotImplementedError()
