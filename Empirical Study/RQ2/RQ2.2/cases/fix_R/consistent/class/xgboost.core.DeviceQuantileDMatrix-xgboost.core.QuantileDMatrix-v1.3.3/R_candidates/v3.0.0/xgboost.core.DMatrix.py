class DMatrix:  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """Data Matrix used in XGBoost.

    DMatrix is an internal data structure that is used by XGBoost, which is optimized
    for both memory efficiency and training speed.  You can construct DMatrix from
    multiple different sources of data.

    """

    @_deprecate_positional_args
    def __init__(
        self,
        data: DataType,
        label: Optional[ArrayLike] = None,
        *,
        weight: Optional[ArrayLike] = None,
        base_margin: Optional[ArrayLike] = None,
        missing: Optional[float] = None,
        silent: bool = False,
        feature_names: Optional[FeatureNames] = None,
        feature_types: Optional[FeatureTypes] = None,
        nthread: Optional[int] = None,
        group: Optional[ArrayLike] = None,
        qid: Optional[ArrayLike] = None,
        label_lower_bound: Optional[ArrayLike] = None,
        label_upper_bound: Optional[ArrayLike] = None,
        feature_weights: Optional[ArrayLike] = None,
        enable_categorical: bool = False,
        data_split_mode: DataSplitMode = DataSplitMode.ROW,
    ) -> None:
        """Parameters
        ----------
        data :
            Data source of DMatrix. See :ref:`py-data` for a list of supported input
            types.

            Note that, if passing an iterator, it **will cache data on disk**, and note
            that fields like ``label`` will be concatenated in-memory from multiple calls
            to the iterator.
        label :
            Label of the training data.
        weight :
            Weight for each instance.

             .. note::

                 For ranking task, weights are per-group.  In ranking task, one weight
                 is assigned to each group (not each data point). This is because we
                 only care about the relative ordering of data points within each group,
                 so it doesn't make sense to assign weights to individual data points.

        base_margin :
            Global bias for each instance. See :doc:`/tutorials/intercept` for details.
        missing :
            Value in the input data which needs to be present as a missing value. If
            None, defaults to np.nan.
        silent :
            Whether print messages during construction
        feature_names :
            Set names for features.
        feature_types :

            Set types for features. If `data` is a DataFrame type and passing
            `enable_categorical=True`, the types will be deduced automatically
            from the column types.

            Otherwise, one can pass a list-like input with the same length as number
            of columns in `data`, with the following possible values:

            - "c", which represents categorical columns.
            - "q", which represents numeric columns.
            - "int", which represents integer columns.
            - "i", which represents boolean columns.

            Note that, while categorical types are treated differently from
            the rest for model fitting purposes, the other types do not influence
            the generated model, but have effects in other functionalities such as
            feature importances.

            For categorical features, the input is assumed to be preprocessed and
            encoded by the users. The encoding can be done via
            :py:class:`sklearn.preprocessing.OrdinalEncoder` or pandas dataframe
            `.cat.codes` method. This is useful when users want to specify categorical
            features without having to construct a dataframe as input.

        nthread :
            Number of threads to use for loading data when parallelization is
            applicable. If -1, uses maximum threads available on the system.
        group :
            Group size for all ranking group.
        qid :
            Query ID for data samples, used for ranking.
        label_lower_bound :
            Lower bound for survival training.
        label_upper_bound :
            Upper bound for survival training.
        feature_weights :
            Set feature weights for column sampling.
        enable_categorical :

            .. versionadded:: 1.3.0

            .. note:: This parameter is experimental

            Experimental support of specializing for categorical features.

            If passing 'True' and 'data' is a data frame (from supported libraries such
            as Pandas, Modin or cuDF), columns of categorical types will automatically
            be set to be of categorical type (feature_type='c') in the resulting
            DMatrix.

            If passing 'False' and 'data' is a data frame with categorical columns,
            it will result in an error being thrown.

            If 'data' is not a data frame, this argument is ignored.

            JSON/UBJSON serialization format is required for this.

        """
        if group is not None and qid is not None:
            raise ValueError("Either one of `group` or `qid` should be None.")

        self.missing = missing if missing is not None else np.nan
        self.nthread = nthread if nthread is not None else -1
        self.silent = silent

        if isinstance(data, ctypes.c_void_p):
            # Used for constructing DMatrix slice.
            self.handle = data
            return

        from .data import _is_iter, dispatch_data_backend

        if _is_iter(data):
            self._init_from_iter(data, enable_categorical)
            assert self.handle is not None
            return

        handle, feature_names, feature_types = dispatch_data_backend(
            data=data,
            missing=self.missing,
            threads=self.nthread,
            feature_names=feature_names,
            feature_types=feature_types,
            enable_categorical=enable_categorical,
            data_split_mode=data_split_mode,
        )
        assert handle is not None
        self.handle = handle

        self.set_info(
            label=label,
            weight=weight,
            base_margin=base_margin,
            group=group,
            qid=qid,
            label_lower_bound=label_lower_bound,
            label_upper_bound=label_upper_bound,
            feature_weights=feature_weights,
        )

        if feature_names is not None:
            self.feature_names = feature_names
        if feature_types is not None:
            self.feature_types = feature_types

    def _init_from_iter(self, it: DataIter, enable_categorical: bool) -> None:
        args = make_jcargs(
            missing=self.missing,
            nthread=self.nthread,
            cache_prefix=it.cache_prefix if it.cache_prefix else "",
            on_host=it.on_host,
            min_cache_page_bytes=it.min_cache_page_bytes,
        )
        handle = ctypes.c_void_p()
        reset_callback, next_callback = it.get_callbacks(enable_categorical)
        ret = _LIB.XGDMatrixCreateFromCallback(
            None,
            it.proxy.handle,
            reset_callback,
            next_callback,
            args,
            ctypes.byref(handle),
        )
        it.reraise()
        # delay check_call to throw intermediate exception first
        _check_call(ret)
        self.handle = handle

    def __del__(self) -> None:
        if hasattr(self, "handle"):
            assert self.handle is not None
            _check_call(_LIB.XGDMatrixFree(self.handle))
            del self.handle

    @_deprecate_positional_args
    def set_info(
        self,
        *,
        label: Optional[ArrayLike] = None,
        weight: Optional[ArrayLike] = None,
        base_margin: Optional[ArrayLike] = None,
        group: Optional[ArrayLike] = None,
        qid: Optional[ArrayLike] = None,
        label_lower_bound: Optional[ArrayLike] = None,
        label_upper_bound: Optional[ArrayLike] = None,
        feature_names: Optional[FeatureNames] = None,
        feature_types: Optional[FeatureTypes] = None,
        feature_weights: Optional[ArrayLike] = None,
    ) -> None:
        """Set meta info for DMatrix.  See doc string for :py:obj:`xgboost.DMatrix`."""
        from .data import dispatch_meta_backend

        if label is not None:
            self.set_label(label)
        if weight is not None:
            self.set_weight(weight)
        if base_margin is not None:
            self.set_base_margin(base_margin)
        if group is not None:
            self.set_group(group)
        if qid is not None:
            self.set_uint_info("qid", qid)
        if label_lower_bound is not None:
            self.set_float_info("label_lower_bound", label_lower_bound)
        if label_upper_bound is not None:
            self.set_float_info("label_upper_bound", label_upper_bound)
        if feature_names is not None:
            self.feature_names = feature_names
        if feature_types is not None:
            self.feature_types = feature_types
        if feature_weights is not None:
            dispatch_meta_backend(
                matrix=self, data=feature_weights, name="feature_weights"
            )

    def get_float_info(self, field: str) -> np.ndarray:
        """Get float property from the DMatrix.

        Parameters
        ----------
        field: str
            The field name of the information

        Returns
        -------
        info : array
            a numpy array of float information of the data
        """
        length = c_bst_ulong()
        ret = ctypes.POINTER(ctypes.c_float)()
        _check_call(
            _LIB.XGDMatrixGetFloatInfo(
                self.handle, c_str(field), ctypes.byref(length), ctypes.byref(ret)
            )
        )
        return ctypes2numpy(ret, length.value, np.float32)

    def get_uint_info(self, field: str) -> np.ndarray:
        """Get unsigned integer property from the DMatrix.

        Parameters
        ----------
        field: str
            The field name of the information

        Returns
        -------
        info : array
            a numpy array of unsigned integer information of the data
        """
        length = c_bst_ulong()
        ret = ctypes.POINTER(ctypes.c_uint)()
        _check_call(
            _LIB.XGDMatrixGetUIntInfo(
                self.handle, c_str(field), ctypes.byref(length), ctypes.byref(ret)
            )
        )
        return ctypes2numpy(ret, length.value, np.uint32)

    def set_float_info(self, field: str, data: ArrayLike) -> None:
        """Set float type property into the DMatrix.

        Parameters
        ----------
        field: str
            The field name of the information

        data: numpy array
            The array of data to be set
        """
        from .data import dispatch_meta_backend

        dispatch_meta_backend(self, data, field, "float")

    def set_float_info_npy2d(self, field: str, data: ArrayLike) -> None:
        """Set float type property into the DMatrix
           for numpy 2d array input

        Parameters
        ----------
        field: str
            The field name of the information

        data: numpy array
            The array of data to be set
        """
        from .data import dispatch_meta_backend

        dispatch_meta_backend(self, data, field, "float")

    def set_uint_info(self, field: str, data: ArrayLike) -> None:
        """Set uint type property into the DMatrix.

        Parameters
        ----------
        field: str
            The field name of the information

        data: numpy array
            The array of data to be set
        """
        from .data import dispatch_meta_backend

        dispatch_meta_backend(self, data, field, "uint32")

    def save_binary(self, fname: PathLike, silent: bool = True) -> None:
        """Save DMatrix to an XGBoost buffer.  Saved binary can be later loaded
        by providing the path to :py:func:`xgboost.DMatrix` as input.

        Parameters
        ----------
        fname : string or os.PathLike
            Name of the output buffer file.
        silent : bool (optional; default: True)
            If set, the output is suppressed.
        """
        fname = os.fspath(os.path.expanduser(fname))
        _check_call(
            _LIB.XGDMatrixSaveBinary(self.handle, c_str(fname), ctypes.c_int(silent))
        )

    def set_label(self, label: ArrayLike) -> None:
        """Set label of dmatrix

        Parameters
        ----------
        label: array like
            The label information to be set into DMatrix
        """
        from .data import dispatch_meta_backend

        dispatch_meta_backend(self, label, "label", "float")

    def set_weight(self, weight: ArrayLike) -> None:
        """Set weight of each instance.

        Parameters
        ----------
        weight : array like
            Weight for each data point

            .. note:: For ranking task, weights are per-group.

                In ranking task, one weight is assigned to each group (not each
                data point). This is because we only care about the relative
                ordering of data points within each group, so it doesn't make
                sense to assign weights to individual data points.

        """
        from .data import dispatch_meta_backend

        dispatch_meta_backend(self, weight, "weight", "float")

    def set_base_margin(self, margin: ArrayLike) -> None:
        """Set base margin of booster to start from.

        This can be used to specify a prediction value of existing model to be
        base_margin However, remember margin is needed, instead of transformed
        prediction e.g. for logistic regression: need to put in value before
        logistic transformation see also example/demo.py

        Parameters
        ----------
        margin: array like
            Prediction margin of each datapoint

        """
        from .data import dispatch_meta_backend

        dispatch_meta_backend(self, margin, "base_margin", "float")

    def set_group(self, group: ArrayLike) -> None:
        """Set group size of DMatrix (used for ranking).

        Parameters
        ----------
        group : array like
            Group size of each group
        """
        from .data import dispatch_meta_backend

        dispatch_meta_backend(self, group, "group", "uint32")

    def get_label(self) -> np.ndarray:
        """Get the label of the DMatrix.

        Returns
        -------
        label : array
        """
        return self.get_float_info("label")

    def get_weight(self) -> np.ndarray:
        """Get the weight of the DMatrix.

        Returns
        -------
        weight : array
        """
        return self.get_float_info("weight")

    def get_base_margin(self) -> np.ndarray:
        """Get the base margin of the DMatrix.

        Returns
        -------
        base_margin
        """
        return self.get_float_info("base_margin")

    def get_group(self) -> np.ndarray:
        """Get the group of the DMatrix.

        Returns
        -------
        group
        """
        group_ptr = self.get_uint_info("group_ptr")
        return np.diff(group_ptr)

    def get_data(self) -> scipy.sparse.csr_matrix:
        """Get the predictors from DMatrix as a CSR matrix. This getter is mostly for
        testing purposes. If this is a quantized DMatrix then quantized values are
        returned instead of input values.

        .. versionadded:: 1.7.0

        """
        indptr = np.empty(self.num_row() + 1, dtype=np.uint64)
        indices = np.empty(self.num_nonmissing(), dtype=np.uint32)
        data = np.empty(self.num_nonmissing(), dtype=np.float32)

        c_indptr = indptr.ctypes.data_as(ctypes.POINTER(c_bst_ulong))
        c_indices = indices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint32))
        c_data = data.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        config = from_pystr_to_cstr(json.dumps({}))

        _check_call(
            _LIB.XGDMatrixGetDataAsCSR(self.handle, config, c_indptr, c_indices, c_data)
        )
        ret = scipy.sparse.csr_matrix(
            (data, indices, indptr), shape=(self.num_row(), self.num_col())
        )
        return ret

    def get_quantile_cut(self) -> Tuple[np.ndarray, np.ndarray]:
        """Get quantile cuts for quantization.

        .. versionadded:: 2.0.0

        """
        n_features = self.num_col()

        c_sindptr = ctypes.c_char_p()
        c_sdata = ctypes.c_char_p()
        config = make_jcargs()
        _check_call(
            _LIB.XGDMatrixGetQuantileCut(
                self.handle, config, ctypes.byref(c_sindptr), ctypes.byref(c_sdata)
            )
        )
        assert c_sindptr.value is not None
        assert c_sdata.value is not None

        i_indptr = json.loads(c_sindptr.value)
        indptr = from_array_interface(i_indptr)
        assert indptr.size == n_features + 1
        assert indptr.dtype == np.uint64

        i_data = json.loads(c_sdata.value)
        data = from_array_interface(i_data)
        assert data.size == indptr[-1]
        assert data.dtype == np.float32
        return indptr, data

    def num_row(self) -> int:
        """Get the number of rows in the DMatrix."""
        ret = c_bst_ulong()
        _check_call(_LIB.XGDMatrixNumRow(self.handle, ctypes.byref(ret)))
        return ret.value

    def num_col(self) -> int:
        """Get the number of columns (features) in the DMatrix."""
        ret = c_bst_ulong()
        _check_call(_LIB.XGDMatrixNumCol(self.handle, ctypes.byref(ret)))
        return ret.value

    def num_nonmissing(self) -> int:
        """Get the number of non-missing values in the DMatrix.

        .. versionadded:: 1.7.0

        """
        ret = c_bst_ulong()
        _check_call(_LIB.XGDMatrixNumNonMissing(self.handle, ctypes.byref(ret)))
        return ret.value

    def data_split_mode(self) -> DataSplitMode:
        """Get the data split mode of the DMatrix.

        .. versionadded:: 2.1.0

        """
        ret = c_bst_ulong()
        _check_call(_LIB.XGDMatrixDataSplitMode(self.handle, ctypes.byref(ret)))
        return DataSplitMode(ret.value)

    def slice(
        self, rindex: Union[List[int], np.ndarray], allow_groups: bool = False
    ) -> "DMatrix":
        """Slice the DMatrix and return a new DMatrix that only contains `rindex`.

        Parameters
        ----------
        rindex
            List of indices to be selected.
        allow_groups
            Allow slicing of a matrix with a groups attribute

        Returns
        -------
        res
            A new DMatrix containing only selected indices.
        """
        from .data import _maybe_np_slice

        handle = ctypes.c_void_p()

        rindex = _maybe_np_slice(rindex, dtype=np.int32)
        _check_call(
            _LIB.XGDMatrixSliceDMatrixEx(
                self.handle,
                c_array(ctypes.c_int, rindex),
                c_bst_ulong(len(rindex)),
                ctypes.byref(handle),
                ctypes.c_int(1 if allow_groups else 0),
            )
        )
        return DMatrix(handle)

    @property
    def feature_names(self) -> Optional[FeatureNames]:
        """Labels for features (column labels).

        Setting it to ``None`` resets existing feature names.

        """
        length = c_bst_ulong()
        sarr = ctypes.POINTER(ctypes.c_char_p)()
        _check_call(
            _LIB.XGDMatrixGetStrFeatureInfo(
                self.handle,
                c_str("feature_name"),
                ctypes.byref(length),
                ctypes.byref(sarr),
            )
        )
        feature_names = from_cstr_to_pystr(sarr, length)
        if not feature_names:
            return None
        return feature_names

    @feature_names.setter
    def feature_names(self, feature_names: Optional[FeatureNames]) -> None:
        if feature_names is None:
            _check_call(
                _LIB.XGDMatrixSetStrFeatureInfo(
                    self.handle, c_str("feature_name"), None, c_bst_ulong(0)
                )
            )
            return

        # validate feature name
        feature_names = _validate_feature_info(
            feature_names,
            self.num_col(),
            self.data_split_mode() == DataSplitMode.COL,
            "feature names",
        )
        if len(feature_names) != len(set(feature_names)):
            values, counts = np.unique(
                feature_names,
                return_index=False,
                return_inverse=False,
                return_counts=True,
            )
            duplicates = [name for name, cnt in zip(values, counts) if cnt > 1]
            raise ValueError(
                f"feature_names must be unique. Duplicates found: {duplicates}"
            )

        # prohibit the use symbols that may affect parsing. e.g. []<
        if not all(
            isinstance(f, str) and not any(x in f for x in ["[", "]", "<"])
            for f in feature_names
        ):
            raise ValueError(
                "feature_names must be string, and may not contain [, ] or <"
            )

        feature_names_bytes = [bytes(f, encoding="utf-8") for f in feature_names]
        c_feature_names = (ctypes.c_char_p * len(feature_names_bytes))(
            *feature_names_bytes
        )
        _check_call(
            _LIB.XGDMatrixSetStrFeatureInfo(
                self.handle,
                c_str("feature_name"),
                c_feature_names,
                c_bst_ulong(len(feature_names)),
            )
        )

    @property
    def feature_types(self) -> Optional[FeatureTypes]:
        """Type of features (column types).

        This is for displaying the results and categorical data support. See
        :py:class:`DMatrix` for details.

        Setting it to ``None`` resets existing feature types.

        """
        length = c_bst_ulong()
        sarr = ctypes.POINTER(ctypes.c_char_p)()
        _check_call(
            _LIB.XGDMatrixGetStrFeatureInfo(
                self.handle,
                c_str("feature_type"),
                ctypes.byref(length),
                ctypes.byref(sarr),
            )
        )
        res = from_cstr_to_pystr(sarr, length)
        if not res:
            return None
        return res

    @feature_types.setter
    def feature_types(self, feature_types: Optional[FeatureTypes]) -> None:
        if feature_types is None:
            # Reset
            _check_call(
                _LIB.XGDMatrixSetStrFeatureInfo(
                    self.handle, c_str("feature_type"), None, c_bst_ulong(0)
                )
            )
            return

        feature_types = _validate_feature_info(
            feature_types,
            self.num_col(),
            self.data_split_mode() == DataSplitMode.COL,
            "feature types",
        )

        feature_types_bytes = [bytes(f, encoding="utf-8") for f in feature_types]
        c_feature_types = (ctypes.c_char_p * len(feature_types_bytes))(
            *feature_types_bytes
        )
        _check_call(
            _LIB.XGDMatrixSetStrFeatureInfo(
                self.handle,
                c_str("feature_type"),
                c_feature_types,
                c_bst_ulong(len(feature_types)),
            )
        )
