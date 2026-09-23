class Booster:
    # pylint: disable=too-many-public-methods
    """A Booster of XGBoost.

    Booster is the model of xgboost, that contains low level routines for
    training, prediction and evaluation.
    """

    def __init__(
        self,
        params: Optional[BoosterParam] = None,
        cache: Optional[Sequence[DMatrix]] = None,
        model_file: Optional[Union["Booster", bytearray, os.PathLike, str]] = None,
    ) -> None:
        # pylint: disable=invalid-name
        """
        Parameters
        ----------
        params :
            Parameters for boosters.
        cache :
            List of cache items.
        model_file :
            Path to the model file if it's string or PathLike.
        """
        cache = cache if cache is not None else []
        for d in cache:
            if not isinstance(d, DMatrix):
                raise TypeError(f"invalid cache item: {type(d).__name__}", cache)

        dmats = c_array(ctypes.c_void_p, [d.handle for d in cache])
        self.handle: Optional[ctypes.c_void_p] = ctypes.c_void_p()
        _check_call(
            _LIB.XGBoosterCreate(
                dmats, c_bst_ulong(len(cache)), ctypes.byref(self.handle)
            )
        )
        for d in cache:
            # Validate feature only after the feature names are saved into booster.
            self._assign_dmatrix_features(d)

        if isinstance(model_file, Booster):
            assert self.handle is not None
            # We use the pickle interface for getting memory snapshot from
            # another model, and load the snapshot with this booster.
            state = model_file.__getstate__()
            handle = state["handle"]
            del state["handle"]
            ptr = (ctypes.c_char * len(handle)).from_buffer(handle)
            length = c_bst_ulong(len(handle))
            _check_call(_LIB.XGBoosterUnserializeFromBuffer(self.handle, ptr, length))
            self.__dict__.update(state)
        elif isinstance(model_file, (str, os.PathLike, bytearray)):
            self.load_model(model_file)
        elif model_file is None:
            pass
        else:
            raise TypeError("Unknown type:", model_file)

        params = params or {}
        params_processed = _configure_metrics(params.copy())
        params_processed = self._configure_constraints(params_processed)
        if isinstance(params_processed, list):
            params_processed.append(("validate_parameters", True))
        else:
            params_processed["validate_parameters"] = True

        self.set_param(params_processed or {})

    def _transform_monotone_constrains(
        self, value: Union[Dict[str, int], str, Tuple[int, ...]]
    ) -> Union[Tuple[int, ...], str]:
        if isinstance(value, str):
            return value
        if isinstance(value, tuple):
            return value

        constrained_features = set(value.keys())
        feature_names = self.feature_names or []
        if not constrained_features.issubset(set(feature_names)):
            raise ValueError(
                "Constrained features are not a subset of training data feature names"
            )

        return tuple(value.get(name, 0) for name in feature_names)

    def _transform_interaction_constraints(
        self, value: Union[Sequence[Sequence[str]], str]
    ) -> Union[str, List[List[int]]]:
        if isinstance(value, str):
            return value
        feature_idx_mapping = {
            name: idx for idx, name in enumerate(self.feature_names or [])
        }

        try:
            result = []
            for constraint in value:
                result.append(
                    [feature_idx_mapping[feature_name] for feature_name in constraint]
                )
            return result
        except KeyError as e:
            raise ValueError(
                "Constrained features are not a subset of training data feature names"
            ) from e

    def _configure_constraints(self, params: BoosterParam) -> BoosterParam:
        if isinstance(params, dict):
            # we must use list in the internal code as there can be multiple metrics
            # with the same parameter name `eval_metric` (same key for dictionary).
            params = list(params.items())
        for idx, param in enumerate(params):
            name, value = param
            if value is None:
                continue

            if name == "monotone_constraints":
                params[idx] = (name, self._transform_monotone_constrains(value))
            elif name == "interaction_constraints":
                params[idx] = (name, self._transform_interaction_constraints(value))

        return params

    def __del__(self) -> None:
        if hasattr(self, "handle") and self.handle is not None:
            _check_call(_LIB.XGBoosterFree(self.handle))
            self.handle = None

    def __getstate__(self) -> Dict:
        # can't pickle ctypes pointers, put model content in bytearray
        this = self.__dict__.copy()
        handle = this["handle"]
        if handle is not None:
            length = c_bst_ulong()
            cptr = ctypes.POINTER(ctypes.c_char)()
            _check_call(
                _LIB.XGBoosterSerializeToBuffer(
                    self.handle, ctypes.byref(length), ctypes.byref(cptr)
                )
            )
            buf = ctypes2buffer(cptr, length.value)
            this["handle"] = buf
        return this

    def __setstate__(self, state: Dict) -> None:
        # reconstruct handle from raw data
        handle = state["handle"]
        if handle is not None:
            buf = handle
            dmats = c_array(ctypes.c_void_p, [])
            handle = ctypes.c_void_p()
            _check_call(
                _LIB.XGBoosterCreate(dmats, c_bst_ulong(0), ctypes.byref(handle))
            )
            length = c_bst_ulong(len(buf))
            ptr = (ctypes.c_char * len(buf)).from_buffer(buf)
            _check_call(_LIB.XGBoosterUnserializeFromBuffer(handle, ptr, length))
            state["handle"] = handle
        self.__dict__.update(state)

    def __getitem__(self, val: Union[Integer, tuple, slice, EllipsisType]) -> "Booster":
        """Get a slice of the tree-based model. Attributes like `best_iteration` and
        `best_score` are removed in the resulting booster.

        .. versionadded:: 1.3.0

        """
        # convert to slice for all other types
        if isinstance(val, (np.integer, int)):
            val = slice(int(val), int(val + 1))
        if isinstance(val, EllipsisType):
            val = slice(0, 0)
        if isinstance(val, tuple):
            raise ValueError("Only supports slicing through 1 dimension.")
        # All supported types are now slice
        if not isinstance(val, slice):
            msg = _expect((int, slice, np.integer, EllipsisType), type(val))
            raise TypeError(msg)

        if isinstance(val.start, EllipsisType) or val.start is None:
            start = 0
        else:
            start = val.start
        if isinstance(val.stop, EllipsisType) or val.stop is None:
            stop = 0
        else:
            stop = val.stop
            if stop < start:
                raise ValueError("Invalid slice", val)

        step = val.step if val.step is not None else 1

        c_start = ctypes.c_int(start)
        c_stop = ctypes.c_int(stop)
        c_step = ctypes.c_int(step)

        sliced_handle = ctypes.c_void_p()
        status = _LIB.XGBoosterSlice(
            self.handle, c_start, c_stop, c_step, ctypes.byref(sliced_handle)
        )
        if status == -2:
            raise IndexError("Layer index out of range")
        _check_call(status)

        sliced = Booster()
        _check_call(_LIB.XGBoosterFree(sliced.handle))
        sliced.handle = sliced_handle
        return sliced

    def __iter__(self) -> Generator["Booster", None, None]:
        """Iterator method for getting individual trees.

        .. versionadded:: 2.0.0

        """
        for i in range(0, self.num_boosted_rounds()):
            yield self[i]

    def save_config(self) -> str:
        """Output internal parameter configuration of Booster as a JSON
        string.

        .. versionadded:: 1.0.0

        """
        json_string = ctypes.c_char_p()
        length = c_bst_ulong()
        _check_call(
            _LIB.XGBoosterSaveJsonConfig(
                self.handle, ctypes.byref(length), ctypes.byref(json_string)
            )
        )
        assert json_string.value is not None
        result = json_string.value.decode()  # pylint: disable=no-member
        return result

    def load_config(self, config: str) -> None:
        """Load configuration returned by `save_config`.

        .. versionadded:: 1.0.0
        """
        assert isinstance(config, str)
        _check_call(_LIB.XGBoosterLoadJsonConfig(self.handle, c_str(config)))

    def __copy__(self) -> "Booster":
        return self.__deepcopy__(None)

    def __deepcopy__(self, _: Any) -> "Booster":
        """Return a copy of booster."""
        return Booster(model_file=self)

    def copy(self) -> "Booster":
        """Copy the booster object.

        Returns
        -------
        booster :
            A copied booster model
        """
        return copy.copy(self)

    def reset(self) -> "Booster":
        """Reset the booster object to release data caches used for training.

        .. versionadded:: 3.0.0

        """
        _check_call(_LIB.XGBoosterReset(self.handle))
        return self

    def attr(self, key: str) -> Optional[str]:
        """Get attribute string from the Booster.

        Parameters
        ----------
        key :
            The key to get attribute from.

        Returns
        -------
        value :
            The attribute value of the key, returns None if attribute do not exist.
        """
        ret = ctypes.c_char_p()
        success = ctypes.c_int()
        _check_call(
            _LIB.XGBoosterGetAttr(
                self.handle, c_str(key), ctypes.byref(ret), ctypes.byref(success)
            )
        )
        if success.value != 0:
            value = ret.value
            assert value
            return py_str(value)
        return None

    def attributes(self) -> Dict[str, Optional[str]]:
        """Get attributes stored in the Booster as a dictionary.

        Returns
        -------
        result : dictionary of  attribute_name: attribute_value pairs of strings.
            Returns an empty dict if there's no attributes.
        """
        length = c_bst_ulong()
        sarr = ctypes.POINTER(ctypes.c_char_p)()
        _check_call(
            _LIB.XGBoosterGetAttrNames(
                self.handle, ctypes.byref(length), ctypes.byref(sarr)
            )
        )
        attr_names = from_cstr_to_pystr(sarr, length)
        return {n: self.attr(n) for n in attr_names}

    def set_attr(self, **kwargs: Optional[Any]) -> None:
        """Set the attribute of the Booster.

        Parameters
        ----------
        **kwargs
            The attributes to set. Setting a value to None deletes an attribute.
        """
        for key, value in kwargs.items():
            c_value = None
            if value is not None:
                c_value = c_str(str(value))
            _check_call(_LIB.XGBoosterSetAttr(self.handle, c_str(key), c_value))

    def _get_feature_info(self, field: str) -> Optional[FeatureInfo]:
        length = c_bst_ulong()
        sarr = ctypes.POINTER(ctypes.c_char_p)()
        if not hasattr(self, "handle") or self.handle is None:
            return None
        _check_call(
            _LIB.XGBoosterGetStrFeatureInfo(
                self.handle,
                c_str(field),
                ctypes.byref(length),
                ctypes.byref(sarr),
            )
        )
        feature_info = from_cstr_to_pystr(sarr, length)
        return feature_info if feature_info else None

    def _set_feature_info(self, features: Optional[FeatureInfo], field: str) -> None:
        if features is not None:
            assert isinstance(features, list)
            feature_info_bytes = [bytes(f, encoding="utf-8") for f in features]
            c_feature_info = (ctypes.c_char_p * len(feature_info_bytes))(
                *feature_info_bytes
            )
            _check_call(
                _LIB.XGBoosterSetStrFeatureInfo(
                    self.handle,
                    c_str(field),
                    c_feature_info,
                    c_bst_ulong(len(features)),
                )
            )
        else:
            _check_call(
                _LIB.XGBoosterSetStrFeatureInfo(
                    self.handle, c_str(field), None, c_bst_ulong(0)
                )
            )

    @property
    def feature_types(self) -> Optional[FeatureTypes]:
        """Feature types for this booster.  Can be directly set by input data or by
        assignment.  See :py:class:`DMatrix` for details.

        """
        return self._get_feature_info("feature_type")

    @feature_types.setter
    def feature_types(self, features: Optional[FeatureTypes]) -> None:
        self._set_feature_info(features, "feature_type")

    @property
    def feature_names(self) -> Optional[FeatureNames]:
        """Feature names for this booster.  Can be directly set by input data or by
        assignment.

        """
        return self._get_feature_info("feature_name")

    @feature_names.setter
    def feature_names(self, features: Optional[FeatureNames]) -> None:
        self._set_feature_info(features, "feature_name")

    def set_param(
        self,
        params: Union[Dict, Iterable[Tuple[str, Any]], str],
        value: Optional[str] = None,
    ) -> None:
        """Set parameters into the Booster.

        Parameters
        ----------
        params :
           list of key,value pairs, dict of key to value or simply str key
        value :
           value of the specified parameter, when params is str key
        """
        if isinstance(params, Mapping):
            params = params.items()
        elif isinstance(params, str) and value is not None:
            params = [(params, value)]
        for key, val in cast(Iterable[Tuple[str, str]], params):
            if isinstance(val, np.ndarray):
                val = val.tolist()
            if val is not None:
                _check_call(
                    _LIB.XGBoosterSetParam(self.handle, c_str(key), c_str(str(val)))
                )

    def update(
        self, dtrain: DMatrix, iteration: int, fobj: Optional[Objective] = None
    ) -> None:
        """Update for one iteration, with objective function calculated
        internally.  This function should not be called directly by users.

        Parameters
        ----------
        dtrain :
            Training data.
        iteration :
            Current iteration number.
        fobj :
            Customized objective function.

        """
        if not isinstance(dtrain, DMatrix):
            raise TypeError(f"invalid training matrix: {type(dtrain).__name__}")
        self._assign_dmatrix_features(dtrain)

        if fobj is None:
            _check_call(
                _LIB.XGBoosterUpdateOneIter(
                    self.handle, ctypes.c_int(iteration), dtrain.handle
                )
            )
        else:
            pred = self.predict(dtrain, output_margin=True, training=True)
            grad, hess = fobj(pred, dtrain)
            self.boost(dtrain, iteration=iteration, grad=grad, hess=hess)

    def boost(
        self, dtrain: DMatrix, iteration: int, grad: NumpyOrCupy, hess: NumpyOrCupy
    ) -> None:
        """Boost the booster for one iteration with customized gradient statistics.
        Like :py:func:`xgboost.Booster.update`, this function should not be called
        directly by users.

        Parameters
        ----------
        dtrain :
            The training DMatrix.
        grad :
            The first order of gradient.
        hess :
            The second order of gradient.

        """
        from .data import _ensure_np_dtype, _is_cupy_alike

        self._assign_dmatrix_features(dtrain)

        def is_flatten(array: NumpyOrCupy) -> bool:
            return len(array.shape) == 1 or array.shape[1] == 1

        def grad_arrinf(array: NumpyOrCupy) -> bytes:
            # Can we check for __array_interface__ instead of a specific type instead?
            msg = (
                "Expecting `np.ndarray` or `cupy.ndarray` for gradient and hessian."
                f" Got: {type(array)}"
            )
            if not isinstance(array, np.ndarray) and not _is_cupy_alike(array):
                raise TypeError(msg)

            n_samples = dtrain.num_row()
            if array.shape[0] != n_samples and is_flatten(array):
                warnings.warn(
                    "Since 2.1.0, the shape of the gradient and hessian is required to"
                    " be (n_samples, n_targets) or (n_samples, n_classes).",
                    FutureWarning,
                )
                array = array.reshape(n_samples, array.size // n_samples)

            if isinstance(array, np.ndarray):
                array, _ = _ensure_np_dtype(array, array.dtype)
                interface = array_interface(array)
            elif _is_cupy_alike(array):
                interface = cuda_array_interface(array)
            else:
                raise TypeError(msg)

            return interface

        _check_call(
            _LIB.XGBoosterTrainOneIter(
                self.handle,
                dtrain.handle,
                iteration,
                grad_arrinf(grad),
                grad_arrinf(hess),
            )
        )

    def eval_set(
        self,
        evals: Sequence[Tuple[DMatrix, str]],
        iteration: int = 0,
        feval: Optional[Metric] = None,
        output_margin: bool = True,
    ) -> str:
        # pylint: disable=invalid-name
        """Evaluate a set of data.

        Parameters
        ----------
        evals :
            List of items to be evaluated.
        iteration :
            Current iteration.
        feval :
            Custom evaluation function.

        Returns
        -------
        result: str
            Evaluation result string.
        """
        for d in evals:
            if not isinstance(d[0], DMatrix):
                raise TypeError(f"expected DMatrix, got {type(d[0]).__name__}")
            if not isinstance(d[1], str):
                raise TypeError(f"expected string, got {type(d[1]).__name__}")
            self._assign_dmatrix_features(d[0])

        dmats = c_array(ctypes.c_void_p, [d[0].handle for d in evals])
        evnames = c_array(ctypes.c_char_p, [c_str(d[1]) for d in evals])
        msg = ctypes.c_char_p()
        _check_call(
            _LIB.XGBoosterEvalOneIter(
                self.handle,
                ctypes.c_int(iteration),
                dmats,
                evnames,
                c_bst_ulong(len(evals)),
                ctypes.byref(msg),
            )
        )
        assert msg.value is not None
        res = msg.value.decode()  # pylint: disable=no-member
        if feval is not None:
            for dmat, evname in evals:
                feval_ret = feval(
                    self.predict(dmat, training=False, output_margin=output_margin),
                    dmat,
                )
                if isinstance(feval_ret, list):
                    for name, val in feval_ret:
                        # pylint: disable=consider-using-f-string
                        res += "\t%s-%s:%f" % (evname, name, val)
                else:
                    name, val = feval_ret
                    # pylint: disable=consider-using-f-string
                    res += "\t%s-%s:%f" % (evname, name, val)
        return res

    def eval(self, data: DMatrix, name: str = "eval", iteration: int = 0) -> str:
        """Evaluate the model on mat.

        Parameters
        ----------
        data :
            The dmatrix storing the input.

        name :
            The name of the dataset.

        iteration :
            The current iteration number.

        Returns
        -------
        result: str
            Evaluation result string.
        """
        self._assign_dmatrix_features(data)
        return self.eval_set([(data, name)], iteration)

    # pylint: disable=too-many-function-args
    @_deprecate_positional_args
    def predict(
        self,
        data: DMatrix,
        *,
        output_margin: bool = False,
        pred_leaf: bool = False,
        pred_contribs: bool = False,
        approx_contribs: bool = False,
        pred_interactions: bool = False,
        validate_features: bool = True,
        training: bool = False,
        iteration_range: IterationRange = (0, 0),
        strict_shape: bool = False,
    ) -> np.ndarray:
        """Predict with data.  The full model will be used unless `iteration_range` is
        specified, meaning user have to either slice the model or use the
        ``best_iteration`` attribute to get prediction from best model returned from
        early stopping.

        .. note::

            See :doc:`Prediction </prediction>` for issues like thread safety and a
            summary of outputs from this function.

        Parameters
        ----------
        data :
            The dmatrix storing the input.

        output_margin :
            Whether to output the raw untransformed margin value.

        pred_leaf :
            When this option is on, the output will be a matrix of (nsample,
            ntrees) with each record indicating the predicted leaf index of
            each sample in each tree.  Note that the leaf index of a tree is
            unique per tree, so you may find leaf 1 in both tree 1 and tree 0.

        pred_contribs :
            When this is True the output will be a matrix of size (nsample,
            nfeats + 1) with each record indicating the feature contributions
            (SHAP values) for that prediction. The sum of all feature
            contributions is equal to the raw untransformed margin value of the
            prediction. Note the final column is the bias term.

        approx_contribs :
            Approximate the contributions of each feature.  Used when ``pred_contribs`` or
            ``pred_interactions`` is set to True.  Changing the default of this parameter
            (False) is not recommended.

        pred_interactions :
            When this is True the output will be a matrix of size (nsample,
            nfeats + 1, nfeats + 1) indicating the SHAP interaction values for
            each pair of features. The sum of each row (or column) of the
            interaction values equals the corresponding SHAP value (from
            pred_contribs), and the sum of the entire matrix equals the raw
            untransformed margin value of the prediction. Note the last row and
            column correspond to the bias term.

        validate_features :
            When this is True, validate that the Booster's and data's
            feature_names are identical.  Otherwise, it is assumed that the
            feature_names are the same.

        training :
            Whether the prediction value is used for training.  This can effect `dart`
            booster, which performs dropouts during training iterations but use all trees
            for inference. If you want to obtain result with dropouts, set this parameter
            to `True`.  Also, the parameter is set to true when obtaining prediction for
            custom objective function.

            .. versionadded:: 1.0.0

        iteration_range :
            Specifies which layer of trees are used in prediction.  For example, if a
            random forest is trained with 100 rounds.  Specifying `iteration_range=(10,
            20)`, then only the forests built during [10, 20) (half open set) rounds are
            used in this prediction.

            .. versionadded:: 1.4.0

        strict_shape :
            When set to True, output shape is invariant to whether classification is used.
            For both value and margin prediction, the output shape is (n_samples,
            n_groups), n_groups == 1 when multi-class is not used.  Default to False, in
            which case the output shape can be (n_samples, ) if multi-class is not used.

            .. versionadded:: 1.4.0

        Returns
        -------
        prediction : numpy array

        """
        if not isinstance(data, DMatrix):
            raise TypeError("Expecting data to be a DMatrix object, got: ", type(data))
        if validate_features:
            fn = data.feature_names
            self._validate_features(fn)
        args = {
            "type": 0,
            "training": training,
            "iteration_begin": int(iteration_range[0]),
            "iteration_end": int(iteration_range[1]),
            "strict_shape": strict_shape,
        }

        def assign_type(t: int) -> None:
            if args["type"] != 0:
                raise ValueError("One type of prediction at a time.")
            args["type"] = t

        if output_margin:
            assign_type(1)
        if pred_contribs:
            assign_type(2 if not approx_contribs else 3)
        if pred_interactions:
            assign_type(4 if not approx_contribs else 5)
        if pred_leaf:
            assign_type(6)
        preds = ctypes.POINTER(ctypes.c_float)()
        shape = ctypes.POINTER(c_bst_ulong)()
        dims = c_bst_ulong()
        _check_call(
            _LIB.XGBoosterPredictFromDMatrix(
                self.handle,
                data.handle,
                from_pystr_to_cstr(json.dumps(args)),
                ctypes.byref(shape),
                ctypes.byref(dims),
                ctypes.byref(preds),
            )
        )
        return _prediction_output(shape, dims, preds, False)

    # pylint: disable=too-many-statements
    @_deprecate_positional_args
    def inplace_predict(
        self,
        data: DataType,
        *,
        iteration_range: IterationRange = (0, 0),
        predict_type: str = "value",
        missing: float = np.nan,
        validate_features: bool = True,
        base_margin: Any = None,
        strict_shape: bool = False,
    ) -> NumpyOrCupy:
        """Run prediction in-place when possible, Unlike :py:meth:`predict` method,
        inplace prediction does not cache the prediction result.

        Calling only ``inplace_predict`` in multiple threads is safe and lock
        free.  But the safety does not hold when used in conjunction with other
        methods. E.g. you can't train the booster in one thread and perform
        prediction in the other.

        .. note::

            If the device ordinal of the input data doesn't match the one configured for
            the booster, data will be copied to the booster device.

        .. code-block:: python

            booster.set_param({"device": "cuda:0"})
            booster.inplace_predict(cupy_array)

            booster.set_param({"device": "cpu"})
            booster.inplace_predict(numpy_array)

        .. versionadded:: 1.1.0

        Parameters
        ----------
        data :
            The input data.
        iteration_range :
            See :py:meth:`predict` for details.
        predict_type :
            * `value` Output model prediction values.
            * `margin` Output the raw untransformed margin value.
        missing :
            See :py:obj:`xgboost.DMatrix` for details.
        validate_features:
            See :py:meth:`xgboost.Booster.predict` for details.
        base_margin:
            See :py:obj:`xgboost.DMatrix` for details.

            .. versionadded:: 1.4.0

        strict_shape:
            See :py:meth:`xgboost.Booster.predict` for details.

            .. versionadded:: 1.4.0

        Returns
        -------
        prediction : numpy.ndarray/cupy.ndarray
            The prediction result.  When input data is on GPU, prediction result is
            stored in a cupy array.

        """
        preds = ctypes.POINTER(ctypes.c_float)()

        # once caching is supported, we can pass id(data) as cache id.
        args = make_jcargs(
            type=1 if predict_type == "margin" else 0,
            training=False,
            iteration_begin=int(iteration_range[0]),
            iteration_end=int(iteration_range[1]),
            missing=missing,
            strict_shape=strict_shape,
            cache_id=0,
        )
        shape = ctypes.POINTER(c_bst_ulong)()
        dims = c_bst_ulong()

        if base_margin is not None:
            proxy: Optional[_ProxyDMatrix] = _ProxyDMatrix()
            assert proxy is not None
            proxy.set_info(base_margin=base_margin)
            p_handle = proxy.handle
        else:
            proxy = None
            p_handle = ctypes.c_void_p()
        assert proxy is None or isinstance(proxy, _ProxyDMatrix)

        from .data import (
            ArrowTransformed,
            PandasTransformed,
            _is_arrow,
            _is_cudf_df,
            _is_cudf_pandas,
            _is_cupy_alike,
            _is_list,
            _is_np_array_like,
            _is_pandas_df,
            _is_pandas_series,
            _is_polars,
            _is_polars_series,
            _is_tuple,
            _transform_arrow_table,
            _transform_pandas_df,
            _transform_polars_df,
        )

        if _is_cudf_pandas(data):
            data = data._fsproxy_fast  # pylint: disable=protected-access

        enable_categorical = True
        if _is_arrow(data):
            data, fns, _ = _transform_arrow_table(data, enable_categorical, None, None)
        if _is_polars_series(data):
            pl = import_polars()
            data = pl.DataFrame({data.name: data})
        if _is_polars(data):
            data, fns, _ = _transform_polars_df(data, enable_categorical, None, None)
        if _is_pandas_series(data):
            import pandas as pd

            data = pd.DataFrame(data)
        if _is_pandas_df(data):
            data, fns, _ = _transform_pandas_df(data, enable_categorical)
            if validate_features:
                self._validate_features(fns)
        if _is_list(data) or _is_tuple(data):
            data = np.array(data)

        if validate_features:
            if not hasattr(data, "shape"):
                raise TypeError(
                    "`shape` attribute is required when `validate_features` is True."
                )
            if len(data.shape) != 1 and self.num_features() != data.shape[1]:
                raise ValueError(
                    f"Feature shape mismatch, expected: {self.num_features()}, "
                    f"got {data.shape[1]}"
                )

        if _is_np_array_like(data):
            from .data import _ensure_np_dtype

            data, _ = _ensure_np_dtype(data, data.dtype)
            _check_call(
                _LIB.XGBoosterPredictFromDense(
                    self.handle,
                    array_interface(data),
                    args,
                    p_handle,
                    ctypes.byref(shape),
                    ctypes.byref(dims),
                    ctypes.byref(preds),
                )
            )
            return _prediction_output(shape, dims, preds, False)
        if isinstance(data, (ArrowTransformed, PandasTransformed)):
            _check_call(
                _LIB.XGBoosterPredictFromColumnar(
                    self.handle,
                    data.array_interface(),
                    args,
                    p_handle,
                    ctypes.byref(shape),
                    ctypes.byref(dims),
                    ctypes.byref(preds),
                )
            )
            return _prediction_output(shape, dims, preds, False)
        if isinstance(data, scipy.sparse.csr_matrix):
            from .data import transform_scipy_sparse

            data = transform_scipy_sparse(data, True)
            _check_call(
                _LIB.XGBoosterPredictFromCSR(
                    self.handle,
                    array_interface(data.indptr),
                    array_interface(data.indices),
                    array_interface(data.data),
                    c_bst_ulong(data.shape[1]),
                    args,
                    p_handle,
                    ctypes.byref(shape),
                    ctypes.byref(dims),
                    ctypes.byref(preds),
                )
            )
            return _prediction_output(shape, dims, preds, False)
        if _is_cupy_alike(data):
            from .data import _transform_cupy_array

            data = _transform_cupy_array(data)
            interface_str = cuda_array_interface(data)
            _check_call(
                _LIB.XGBoosterPredictFromCudaArray(
                    self.handle,
                    interface_str,
                    args,
                    p_handle,
                    ctypes.byref(shape),
                    ctypes.byref(dims),
                    ctypes.byref(preds),
                )
            )
            return _prediction_output(shape, dims, preds, True)
        if _is_cudf_df(data):
            from .data import _cudf_array_interfaces, _transform_cudf_df

            data, cat_codes, fns, _ = _transform_cudf_df(
                data, None, None, enable_categorical
            )
            interfaces_str = _cudf_array_interfaces(data, cat_codes)
            if validate_features:
                self._validate_features(fns)
            _check_call(
                _LIB.XGBoosterPredictFromCudaColumnar(
                    self.handle,
                    interfaces_str,
                    args,
                    p_handle,
                    ctypes.byref(shape),
                    ctypes.byref(dims),
                    ctypes.byref(preds),
                )
            )
            return _prediction_output(shape, dims, preds, True)

        raise TypeError(
            "Data type:" + str(type(data)) + " not supported by inplace prediction."
        )

    def save_model(self, fname: PathLike) -> None:
        """Save the model to a file.

        The model is saved in an XGBoost internal format which is universal among the
        various XGBoost interfaces. Auxiliary attributes of the Python Booster object
        (such as feature_names) are only saved when using JSON or UBJSON (default)
        format. Also, parameters that are not part of the model (like metrics,
        `max_depth`, etc) are not saved, see :doc:`Model IO </tutorials/saving_model>`
        for more info.

        .. code-block:: python

          model.save_model("model.json")
          # or
          model.save_model("model.ubj")

        Parameters
        ----------
        fname :
            Output file name

        """
        if isinstance(fname, (str, os.PathLike)):  # assume file name
            fname = os.fspath(os.path.expanduser(fname))
            _check_call(_LIB.XGBoosterSaveModel(self.handle, c_str(fname)))
        else:
            raise TypeError("fname must be a string or os PathLike")

    def save_raw(self, raw_format: str = "ubj") -> bytearray:
        """Save the model to a in memory buffer representation instead of file.

        The model is saved in an XGBoost internal format which is universal among the
        various XGBoost interfaces. Auxiliary attributes of the Python Booster object
        (such as feature_names) are only saved when using JSON or UBJSON (default)
        format. Also, parameters that are not part of the model (like metrics,
        `max_depth`, etc) are not saved, see :doc:`Model IO </tutorials/saving_model>`
        for more info.

        Parameters
        ----------
        raw_format :
            Format of output buffer. Can be `json` or `ubj`.

        Returns
        -------
        An in memory buffer representation of the model

        """
        length = c_bst_ulong()
        cptr = ctypes.POINTER(ctypes.c_char)()
        config = make_jcargs(format=raw_format)
        _check_call(
            _LIB.XGBoosterSaveModelToBuffer(
                self.handle, config, ctypes.byref(length), ctypes.byref(cptr)
            )
        )
        return ctypes2buffer(cptr, length.value)

    def load_model(self, fname: ModelIn) -> None:
        """Load the model from a file or a bytearray.

        The model is saved in an XGBoost internal format which is universal among the
        various XGBoost interfaces. Auxiliary attributes of the Python Booster object
        (such as feature_names) are only saved when using JSON or UBJSON (default)
        format. Also, parameters that are not part of the model (like metrics,
        `max_depth`, etc) are not saved, see :doc:`Model IO </tutorials/saving_model>`
        for more info.

        .. code-block:: python

          model.save_model("model.json")
          model.load_model("model.json")

          # or
          model.save_model("model.ubj")
          model.load_model("model.ubj")

          # or
          buf = model.save_raw()
          model.load_model(buf)

        Parameters
        ----------
        fname :
            Input file name or memory buffer(see also save_raw)

        """

        def is_pathlike(path: ModelIn) -> TypeGuard[os.PathLike[str]]:
            return isinstance(path, os.PathLike)

        if isinstance(fname, str) or is_pathlike(fname):
            # assume file name, cannot use os.path.exist to check, file can be from URL.
            fname = os.fspath(os.path.expanduser(fname))
            _check_call(_LIB.XGBoosterLoadModel(self.handle, c_str(fname)))
        elif isinstance(fname, bytearray):
            buf = fname
            length = c_bst_ulong(len(buf))
            ptr = (ctypes.c_char * len(buf)).from_buffer(buf)
            _check_call(_LIB.XGBoosterLoadModelFromBuffer(self.handle, ptr, length))
        else:
            raise TypeError("Unknown file type: ", fname)

    @property
    def best_iteration(self) -> int:
        """The best iteration during training."""
        best = self.attr("best_iteration")
        if best is not None:
            return int(best)

        raise AttributeError(
            "`best_iteration` is only defined when early stopping is used."
        )

    @best_iteration.setter
    def best_iteration(self, iteration: int) -> None:
        self.set_attr(best_iteration=iteration)

    @property
    def best_score(self) -> float:
        """The best evaluation score during training."""
        best = self.attr("best_score")
        if best is not None:
            return float(best)

        raise AttributeError(
            "`best_score` is only defined when early stopping is used."
        )

    @best_score.setter
    def best_score(self, score: int) -> None:
        self.set_attr(best_score=score)

    def num_boosted_rounds(self) -> int:
        """Get number of boosted rounds.  For gblinear this is reset to 0 after
        serializing the model.

        """
        rounds = ctypes.c_int()
        assert self.handle is not None
        _check_call(_LIB.XGBoosterBoostedRounds(self.handle, ctypes.byref(rounds)))
        return rounds.value

    def num_features(self) -> int:
        """Number of features in booster."""
        features = c_bst_ulong()
        assert self.handle is not None
        _check_call(_LIB.XGBoosterGetNumFeature(self.handle, ctypes.byref(features)))
        return features.value

    def dump_model(
        self,
        fout: PathLike,
        fmap: PathLike = "",
        with_stats: bool = False,
        dump_format: str = "text",
    ) -> None:
        """Dump model into a text or JSON file.  Unlike :py:meth:`save_model`, the
        output format is primarily used for visualization or interpretation,
        hence it's more human readable but cannot be loaded back to XGBoost.

        Parameters
        ----------
        fout :
            Output file name.
        fmap :
            Name of the file containing feature map names.
        with_stats :
            Controls whether the split statistics are output.
        dump_format :
            Format of model dump file. Can be 'text' or 'json'.
        """
        if isinstance(fout, (str, os.PathLike)):
            fout = os.fspath(os.path.expanduser(fout))
            # pylint: disable=consider-using-with
            fout_obj = open(fout, "w", encoding="utf-8")
            need_close = True
        else:
            fout_obj = fout
            need_close = False
        ret = self.get_dump(fmap, with_stats, dump_format)
        if dump_format == "json":
            fout_obj.write("[\n")
            for i, val in enumerate(ret):
                fout_obj.write(val)
                if i < len(ret) - 1:
                    fout_obj.write(",\n")
            fout_obj.write("\n]")
        else:
            for i, val in enumerate(ret):
                fout_obj.write(f"booster[{i}]:\n")
                fout_obj.write(val)
        if need_close:
            fout_obj.close()

    def get_dump(
        self,
        fmap: PathLike = "",
        with_stats: bool = False,
        dump_format: str = "text",
    ) -> List[str]:
        """Returns the model dump as a list of strings.  Unlike :py:meth:`save_model`,
        the output format is primarily used for visualization or interpretation, hence
        it's more human readable but cannot be loaded back to XGBoost.

        Parameters
        ----------
        fmap :
            Name of the file containing feature map names.
        with_stats :
            Controls whether the split statistics should be included.
        dump_format :
            Format of model dump. Can be 'text', 'json' or 'dot'.

        """
        fmap = os.fspath(os.path.expanduser(fmap))
        length = c_bst_ulong()
        sarr = ctypes.POINTER(ctypes.c_char_p)()
        _check_call(
            _LIB.XGBoosterDumpModelEx(
                self.handle,
                c_str(fmap),
                ctypes.c_int(with_stats),
                c_str(dump_format),
                ctypes.byref(length),
                ctypes.byref(sarr),
            )
        )
        res = from_cstr_to_pystr(sarr, length)
        return res

    def get_fscore(self, fmap: PathLike = "") -> Dict[str, Union[float, List[float]]]:
        """Get feature importance of each feature.

        .. note:: Zero-importance features will not be included

           Keep in mind that this function does not include zero-importance feature, i.e.
           those features that have not been used in any split conditions.

        Parameters
        ----------
        fmap :
           The name of feature map file
        """

        return self.get_score(fmap, importance_type="weight")

    def get_score(
        self, fmap: PathLike = "", importance_type: str = "weight"
    ) -> Dict[str, Union[float, List[float]]]:
        """Get feature importance of each feature.
        For tree model Importance type can be defined as:

        * 'weight': the number of times a feature is used to split the data across all trees.
        * 'gain': the average gain across all splits the feature is used in.
        * 'cover': the average coverage across all splits the feature is used in.
        * 'total_gain': the total gain across all splits the feature is used in.
        * 'total_cover': the total coverage across all splits the feature is used in.

        .. note::

           For linear model, only "weight" is defined and it's the normalized coefficients
           without bias.

        .. note:: Zero-importance features will not be included

           Keep in mind that this function does not include zero-importance feature, i.e.
           those features that have not been used in any split conditions.

        Parameters
        ----------
        fmap :
           The name of feature map file.
        importance_type :
            One of the importance types defined above.

        Returns
        -------
        A map between feature names and their scores.  When `gblinear` is used for
        multi-class classification the scores for each feature is a list with length
        `n_classes`, otherwise they're scalars.
        """
        fmap = os.fspath(os.path.expanduser(fmap))
        features = ctypes.POINTER(ctypes.c_char_p)()
        scores = ctypes.POINTER(ctypes.c_float)()
        n_out_features = c_bst_ulong()
        out_dim = c_bst_ulong()
        shape = ctypes.POINTER(c_bst_ulong)()

        _check_call(
            _LIB.XGBoosterFeatureScore(
                self.handle,
                make_jcargs(importance_type=importance_type, feature_map=fmap),
                ctypes.byref(n_out_features),
                ctypes.byref(features),
                ctypes.byref(out_dim),
                ctypes.byref(shape),
                ctypes.byref(scores),
            )
        )
        features_arr = from_cstr_to_pystr(features, n_out_features)
        scores_arr = _prediction_output(shape, out_dim, scores, False)

        results: Dict[str, Union[float, List[float]]] = {}
        if len(scores_arr.shape) > 1 and scores_arr.shape[1] > 1:
            for feat, score in zip(features_arr, scores_arr):
                results[feat] = [float(s) for s in score]
        else:
            for feat, score in zip(features_arr, scores_arr):
                results[feat] = float(score)
        return results

    # pylint: disable=too-many-statements
    def trees_to_dataframe(self, fmap: PathLike = "") -> DataFrame:
        """Parse a boosted tree model text dump into a pandas DataFrame structure.

        This feature is only defined when the decision tree model is chosen as base
        learner (`booster in {gbtree, dart}`). It is not defined for other base learner
        types, such as linear learners (`booster=gblinear`).

        Parameters
        ----------
        fmap :
           The name of feature map file.
        """
        # pylint: disable=too-many-locals
        fmap = os.fspath(os.path.expanduser(fmap))
        if not PANDAS_INSTALLED:
            raise ImportError(
                (
                    "pandas must be available to use this method."
                    "Install pandas before calling again."
                )
            )
        booster = json.loads(self.save_config())["learner"]["gradient_booster"]["name"]
        if booster not in {"gbtree", "dart"}:
            raise ValueError(f"This method is not defined for Booster type {booster}")

        tree_ids = []
        node_ids = []
        fids = []
        splits: List[Union[float, str]] = []
        categories: List[Union[Optional[float], List[str]]] = []
        y_directs: List[Union[float, str]] = []
        n_directs: List[Union[float, str]] = []
        missings: List[Union[float, str]] = []
        gains = []
        covers = []

        trees = self.get_dump(fmap, with_stats=True)
        for i, tree in enumerate(trees):
            for line in tree.split("\n"):
                arr = line.split("[")
                # Leaf node
                if len(arr) == 1:
                    # Last element of line.split is an empty string
                    if arr == [""]:
                        continue
                    # parse string
                    parse = arr[0].split(":")
                    stats = re.split("=|,", parse[1])

                    # append to lists
                    tree_ids.append(i)
                    node_ids.append(int(re.findall(r"\b\d+\b", parse[0])[0]))
                    fids.append("Leaf")
                    splits.append(float("NAN"))
                    categories.append(float("NAN"))
                    y_directs.append(float("NAN"))
                    n_directs.append(float("NAN"))
                    missings.append(float("NAN"))
                    gains.append(float(stats[1]))
                    covers.append(float(stats[3]))
                # Not a Leaf Node
                else:
                    # parse string
                    fid = arr[1].split("]")
                    if fid[0].find("<") != -1:
                        # numerical
                        parse = fid[0].split("<")
                        splits.append(float(parse[1]))
                        categories.append(None)
                    elif fid[0].find(":{") != -1:
                        # categorical
                        parse = fid[0].split(":")
                        cats = parse[1][1:-1]  # strip the {}
                        cats_split = cats.split(",")
                        splits.append(float("NAN"))
                        categories.append(cats_split if cats_split else None)
                    else:
                        raise ValueError("Failed to parse model text dump.")
                    stats = re.split("=|,", fid[1])

                    # append to lists
                    tree_ids.append(i)
                    node_ids.append(int(re.findall(r"\b\d+\b", arr[0])[0]))
                    fids.append(parse[0])
                    str_i = str(i)
                    y_directs.append(str_i + "-" + stats[1])
                    n_directs.append(str_i + "-" + stats[3])
                    missings.append(str_i + "-" + stats[5])
                    gains.append(float(stats[7]))
                    covers.append(float(stats[9]))

        ids = [str(t_id) + "-" + str(n_id) for t_id, n_id in zip(tree_ids, node_ids)]
        df = DataFrame(
            {
                "Tree": tree_ids,
                "Node": node_ids,
                "ID": ids,
                "Feature": fids,
                "Split": splits,
                "Yes": y_directs,
                "No": n_directs,
                "Missing": missings,
                "Gain": gains,
                "Cover": covers,
                "Category": categories,
            }
        )

        return df.sort_values(["Tree", "Node"]).reset_index(drop=True)

    def _assign_dmatrix_features(self, data: DMatrix) -> None:
        if data.num_row() == 0:
            return

        fn = data.feature_names
        ft = data.feature_types

        if self.feature_names is None:
            self.feature_names = fn
        if self.feature_types is None:
            self.feature_types = ft

        self._validate_features(fn)

    def _validate_features(self, feature_names: Optional[FeatureNames]) -> None:
        if self.feature_names is None:
            return

        if feature_names is None and self.feature_names is not None:
            raise ValueError(
                "data did not contain feature names, but the following fields are expected: "
                + ", ".join(self.feature_names)
            )

        if self.feature_names != feature_names:
            dat_missing = set(cast(FeatureNames, self.feature_names)) - set(
                cast(FeatureNames, feature_names)
            )
            my_missing = set(cast(FeatureNames, feature_names)) - set(
                cast(FeatureNames, self.feature_names)
            )

            msg = "feature_names mismatch: {0} {1}"

            if dat_missing:
                msg += (
                    "\nexpected "
                    + ", ".join(str(s) for s in dat_missing)
                    + " in input data"
                )

            if my_missing:
                msg += (
                    "\ntraining data did not have the following fields: "
                    + ", ".join(str(s) for s in my_missing)
                )

            raise ValueError(msg.format(self.feature_names, feature_names))

    def get_split_value_histogram(
        self,
        feature: str,
        fmap: PathLike = "",
        bins: Optional[int] = None,
        as_pandas: bool = True,
    ) -> Union[np.ndarray, DataFrame]:
        """Get split value histogram of a feature

        Parameters
        ----------
        feature :
            The name of the feature.
        fmap:
            The name of feature map file.
        bin :
            The maximum number of bins.
            Number of bins equals number of unique split values n_unique,
            if bins == None or bins > n_unique.
        as_pandas :
            Return pd.DataFrame when pandas is installed.
            If False or pandas is not installed, return numpy ndarray.

        Returns
        -------
        a histogram of used splitting values for the specified feature
        either as numpy array or pandas DataFrame.
        """
        from .data import CAT_T

        xgdump = self.get_dump(fmap=fmap)
        values = []
        # pylint: disable=consider-using-f-string
        regexp = re.compile(r"\[{0}<([\d.Ee+-]+)\]".format(feature))
        for val in xgdump:
            m = re.findall(regexp, val)
            values.extend([float(x) for x in m])

        n_unique = len(np.unique(values))
        bins = max(min(n_unique, bins) if bins is not None else n_unique, 1)

        nph = np.histogram(values, bins=bins)
        nph_stacked = np.column_stack((nph[1][1:], nph[0]))
        nph_stacked = nph_stacked[nph_stacked[:, 1] > 0]

        if nph_stacked.size == 0:
            ft = self.feature_types
            fn = self.feature_names
            if fn is None:
                # Let xgboost generate the feature names.
                fn = [f"f{i}" for i in range(self.num_features())]
            try:
                index = fn.index(feature)
                feature_t: Optional[str] = cast(List[str], ft)[index]
            except (ValueError, AttributeError, TypeError):
                # None.index: attr err, None[0]: type err, fn.index(-1): value err
                feature_t = None
            if feature_t == CAT_T:  # categorical
                raise ValueError(
                    "Split value historgam doesn't support categorical split."
                )

        if as_pandas and PANDAS_INSTALLED:
            return DataFrame(nph_stacked, columns=["SplitValue", "Count"])
        if as_pandas and not PANDAS_INSTALLED:
            warnings.warn(
                "Returning histogram as ndarray"
                " (as_pandas == True, but pandas is not installed).",
                UserWarning,
            )
        return nph_stacked
