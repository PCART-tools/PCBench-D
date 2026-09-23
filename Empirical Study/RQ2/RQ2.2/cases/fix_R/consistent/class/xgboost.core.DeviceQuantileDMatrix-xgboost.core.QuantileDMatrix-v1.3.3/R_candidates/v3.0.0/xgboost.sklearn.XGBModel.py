@xgboost_model_doc(
    """Implementation of the Scikit-Learn API for XGBoost.""",
    ["estimators", "model", "objective"],
)
class XGBModel(XGBModelBase):
    # pylint: disable=too-many-arguments, too-many-instance-attributes, missing-docstring
    @_deprecate_positional_args
    def __init__(
        self,
        *,
        max_depth: Optional[int] = None,
        max_leaves: Optional[int] = None,
        max_bin: Optional[int] = None,
        grow_policy: Optional[str] = None,
        learning_rate: Optional[float] = None,
        n_estimators: Optional[int] = None,
        verbosity: Optional[int] = None,
        objective: SklObjective = None,
        booster: Optional[str] = None,
        tree_method: Optional[str] = None,
        n_jobs: Optional[int] = None,
        gamma: Optional[float] = None,
        min_child_weight: Optional[float] = None,
        max_delta_step: Optional[float] = None,
        subsample: Optional[float] = None,
        sampling_method: Optional[str] = None,
        colsample_bytree: Optional[float] = None,
        colsample_bylevel: Optional[float] = None,
        colsample_bynode: Optional[float] = None,
        reg_alpha: Optional[float] = None,
        reg_lambda: Optional[float] = None,
        scale_pos_weight: Optional[float] = None,
        base_score: Optional[float] = None,
        random_state: Optional[
            Union[np.random.RandomState, np.random.Generator, int]
        ] = None,
        missing: float = np.nan,
        num_parallel_tree: Optional[int] = None,
        monotone_constraints: Optional[Union[Dict[str, int], str]] = None,
        interaction_constraints: Optional[Union[str, Sequence[Sequence[str]]]] = None,
        importance_type: Optional[str] = None,
        device: Optional[str] = None,
        validate_parameters: Optional[bool] = None,
        enable_categorical: bool = False,
        feature_types: Optional[FeatureTypes] = None,
        feature_weights: Optional[ArrayLike] = None,
        max_cat_to_onehot: Optional[int] = None,
        max_cat_threshold: Optional[int] = None,
        multi_strategy: Optional[str] = None,
        eval_metric: Optional[Union[str, List[str], Callable]] = None,
        early_stopping_rounds: Optional[int] = None,
        callbacks: Optional[List[TrainingCallback]] = None,
        **kwargs: Any,
    ) -> None:
        if not SKLEARN_INSTALLED:
            raise ImportError(
                "sklearn needs to be installed in order to use this module"
            )
        self.n_estimators = n_estimators
        self.objective = objective

        self.max_depth = max_depth
        self.max_leaves = max_leaves
        self.max_bin = max_bin
        self.grow_policy = grow_policy
        self.learning_rate = learning_rate
        self.verbosity = verbosity
        self.booster = booster
        self.tree_method = tree_method
        self.gamma = gamma
        self.min_child_weight = min_child_weight
        self.max_delta_step = max_delta_step
        self.subsample = subsample
        self.sampling_method = sampling_method
        self.colsample_bytree = colsample_bytree
        self.colsample_bylevel = colsample_bylevel
        self.colsample_bynode = colsample_bynode
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lambda
        self.scale_pos_weight = scale_pos_weight
        self.base_score = base_score
        self.missing = missing
        self.num_parallel_tree = num_parallel_tree
        self.random_state = random_state
        self.n_jobs = n_jobs
        self.monotone_constraints = monotone_constraints
        self.interaction_constraints = interaction_constraints
        self.importance_type = importance_type
        self.device = device
        self.validate_parameters = validate_parameters
        self.enable_categorical = enable_categorical
        self.feature_types = feature_types
        self.feature_weights = feature_weights
        self.max_cat_to_onehot = max_cat_to_onehot
        self.max_cat_threshold = max_cat_threshold
        self.multi_strategy = multi_strategy
        self.eval_metric = eval_metric
        self.early_stopping_rounds = early_stopping_rounds
        self.callbacks = callbacks
        if kwargs:
            self.kwargs = kwargs

    def _more_tags(self) -> Dict[str, bool]:
        """Tags used for scikit-learn data validation."""
        tags = {"allow_nan": True, "no_validation": True, "sparse": True}
        if hasattr(self, "kwargs") and self.kwargs.get("updater") == "shotgun":
            tags["non_deterministic"] = True

        tags["categorical"] = self.enable_categorical
        return tags

    @staticmethod
    def _update_sklearn_tags_from_dict(
        *,
        tags: _sklearn_Tags,
        tags_dict: Dict[str, bool],
    ) -> _sklearn_Tags:
        """Update ``sklearn.utils.Tags`` inherited from ``scikit-learn`` base classes.

        ``scikit-learn`` 1.6 introduced a dataclass-based interface for estimator tags.
        ref: https://github.com/scikit-learn/scikit-learn/pull/29677

        This method handles updating that instance based on the values in
        ``self._more_tags()``.

        """
        tags.non_deterministic = tags_dict.get("non_deterministic", False)
        tags.no_validation = tags_dict["no_validation"]
        tags.input_tags.allow_nan = tags_dict["allow_nan"]
        tags.input_tags.sparse = tags_dict["sparse"]
        tags.input_tags.categorical = tags_dict["categorical"]
        return tags

    def __sklearn_tags__(self) -> _sklearn_Tags:
        # XGBModelBase.__sklearn_tags__() cannot be called unconditionally,
        # because that method isn't defined for scikit-learn<1.6
        if not hasattr(XGBModelBase, "__sklearn_tags__"):
            err_msg = (
                "__sklearn_tags__() should not be called when using scikit-learn<1.6. "
                f"Detected version: {_sklearn_version}"
            )
            raise AttributeError(err_msg)

        # take whatever tags are provided by BaseEstimator, then modify
        # them with XGBoost-specific values
        return self._update_sklearn_tags_from_dict(
            tags=super().__sklearn_tags__(),  # pylint: disable=no-member
            tags_dict=self._more_tags(),
        )

    def __sklearn_is_fitted__(self) -> bool:
        return hasattr(self, "_Booster")

    @property
    def _doc_link_module(self) -> str:
        return "xgboost"

    @property
    def _doc_link_template(self) -> str:
        ver = _py_version()
        (major, minor, _), post = _parse_version(ver)

        if post == "dev":
            rel = "latest"
        else:
            # RTD tracks the release branch. We don't have independent branches for
            # patch releases.
            rel = f"release_{major}.{minor}.0"

        module = self.__class__.__module__
        # All sklearn estimators are forwarded to the top level module in both source
        # code and sphinx api doc.
        if module == "xgboost.sklearn":
            module = module.split(".")[0]
        name = self.__class__.__name__

        base = "https://xgboost.readthedocs.io/en"
        return f"{base}/{rel}/python/python_api.html#{module}.{name}"

    def _wrapper_params(self) -> Set[str]:
        wrapper_specific = {
            "importance_type",
            "kwargs",
            "missing",
            "n_estimators",
            "enable_categorical",
            "early_stopping_rounds",
            "callbacks",
            "feature_types",
            "feature_weights",
        }
        return wrapper_specific

    def get_booster(self) -> Booster:
        """Get the underlying xgboost Booster of this model.

        This will raise an exception when fit was not called

        Returns
        -------
        booster : a xgboost booster of underlying model
        """
        if not self.__sklearn_is_fitted__():
            from sklearn.exceptions import NotFittedError

            raise NotFittedError("need to call fit or load_model beforehand")
        return self._Booster

    def set_params(self, **params: Any) -> "XGBModel":
        """Set the parameters of this estimator.  Modification of the sklearn method to
        allow unknown kwargs. This allows using the full range of xgboost
        parameters that are not defined as member variables in sklearn grid
        search.

        Returns
        -------
        self

        """
        if not params:
            # Simple optimization to gain speed (inspect is slow)
            return self

        # this concatenates kwargs into parameters, enabling `get_params` for
        # obtaining parameters from keyword parameters.
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                if not hasattr(self, "kwargs"):
                    self.kwargs = {}
                self.kwargs[key] = value

        if self.__sklearn_is_fitted__():
            parameters = self.get_xgb_params()
            self.get_booster().set_param(parameters)

        return self

    def get_params(self, deep: bool = True) -> Dict[str, Any]:
        # pylint: disable=attribute-defined-outside-init
        """Get parameters."""
        # Based on: https://stackoverflow.com/questions/59248211
        # The basic flow in `get_params` is:
        # 0. Return parameters in subclass (self.__class__) first, by using inspect.
        # 1. Return parameters in all parent classes (especially `XGBModel`).
        # 2. Return whatever in `**kwargs`.
        # 3. Merge them.
        #
        # This needs to accommodate being called recursively in the following
        # inheritance graphs (and similar for classification and ranking):
        #
        #   XGBRFRegressor -> XGBRegressor -> XGBModel -> BaseEstimator
        #                     XGBRegressor -> XGBModel -> BaseEstimator
        #                                     XGBModel -> BaseEstimator
        #
        params = super().get_params(deep)
        cp = copy.copy(self)
        # If the immediate parent defines get_params(), use that.
        if callable(getattr(cp.__class__.__bases__[0], "get_params", None)):
            cp.__class__ = cp.__class__.__bases__[0]
        # Otherwise, skip it and assume the next class will have it.
        # This is here primarily for cases where the first class in MRO is a scikit-learn mixin.
        else:
            cp.__class__ = cp.__class__.__bases__[1]
        params.update(cp.__class__.get_params(cp, deep))
        # if kwargs is a dict, update params accordingly
        if hasattr(self, "kwargs") and isinstance(self.kwargs, dict):
            params.update(self.kwargs)
        if isinstance(params["random_state"], np.random.RandomState):
            params["random_state"] = params["random_state"].randint(
                np.iinfo(np.int32).max
            )
        elif isinstance(params["random_state"], np.random.Generator):
            params["random_state"] = int(
                params["random_state"].integers(np.iinfo(np.int32).max)
            )

        return params

    def get_xgb_params(self) -> Dict[str, Any]:
        """Get xgboost specific parameters."""
        params: Dict[str, Any] = self.get_params()

        # Parameters that should not go into native learner.
        wrapper_specific = self._wrapper_params()
        filtered = {}
        for k, v in params.items():
            if k not in wrapper_specific and not callable(v):
                filtered[k] = v

        return filtered

    def get_num_boosting_rounds(self) -> int:
        """Gets the number of xgboost boosting rounds."""
        return DEFAULT_N_ESTIMATORS if self.n_estimators is None else self.n_estimators

    def _get_type(self) -> str:
        if not hasattr(self, "_estimator_type"):
            raise TypeError(
                "`_estimator_type` undefined.  "
                "Please use appropriate mixin to define estimator type."
            )
        return self._estimator_type  # pylint: disable=no-member

    def save_model(self, fname: Union[str, os.PathLike]) -> None:
        meta: Dict[str, Any] = {}
        # For validation.
        meta["_estimator_type"] = self._get_type()
        meta_str = json.dumps(meta)
        self.get_booster().set_attr(scikit_learn=meta_str)
        self.get_booster().save_model(fname)
        self.get_booster().set_attr(scikit_learn=None)

    save_model.__doc__ = f"""{Booster.save_model.__doc__}"""

    def load_model(self, fname: ModelIn) -> None:
        # pylint: disable=attribute-defined-outside-init
        if not self.__sklearn_is_fitted__():
            self._Booster = Booster({"n_jobs": self.n_jobs})
        self.get_booster().load_model(fname)

        meta_str = self.get_booster().attr("scikit_learn")
        if meta_str is not None:
            meta = json.loads(meta_str)
            t = meta.get("_estimator_type", None)
            if t is not None and t != self._get_type():
                raise TypeError(
                    "Loading an estimator with different type. Expecting: "
                    f"{self._get_type()}, got: {t}"
                )

        self.feature_types = self.get_booster().feature_types
        self.get_booster().set_attr(scikit_learn=None)
        config = json.loads(self.get_booster().save_config())
        self._load_model_attributes(config)

    load_model.__doc__ = f"""{Booster.load_model.__doc__}"""

    def _load_model_attributes(self, config: dict) -> None:
        """Load model attributes without hyper-parameters."""
        from sklearn.base import is_classifier

        booster = self.get_booster()

        self.objective = config["learner"]["objective"]["name"]
        self.booster = config["learner"]["gradient_booster"]["name"]
        self.base_score = config["learner"]["learner_model_param"]["base_score"]
        self.feature_types = booster.feature_types

        if is_classifier(self):
            self.n_classes_ = int(config["learner"]["learner_model_param"]["num_class"])
            # binary classification is treated as regression in XGBoost.
            self.n_classes_ = 2 if self.n_classes_ < 2 else self.n_classes_

    # pylint: disable=too-many-branches
    def _configure_fit(
        self,
        booster: Optional[Union[Booster, "XGBModel", str]],
        params: Dict[str, Any],
        feature_weights: Optional[ArrayLike],
    ) -> Tuple[
        Optional[Union[Booster, str, "XGBModel"]],
        Optional[Metric],
        Dict[str, Any],
        Optional[ArrayLike],
    ]:
        """Configure parameters for :py:meth:`fit`."""
        if isinstance(booster, XGBModel):
            model: Optional[Union[Booster, str]] = booster.get_booster()
        else:
            model = booster

        def _deprecated(parameter: str) -> None:
            warnings.warn(
                f"`{parameter}` in `fit` method is deprecated for better compatibility "
                f"with scikit-learn, use `{parameter}` in constructor or`set_params` "
                "instead.",
                UserWarning,
            )

        def _duplicated(parameter: str) -> None:
            raise ValueError(
                f"2 different `{parameter}` are provided.  Use the one in constructor "
                "or `set_params` instead."
            )

        # - configure callable evaluation metric
        metric: Optional[Metric] = None
        if self.eval_metric is not None:
            if callable(self.eval_metric):
                if self._get_type() == "ranker":
                    metric = ltr_metric_decorator(self.eval_metric, self.n_jobs)
                else:
                    metric = _metric_decorator(self.eval_metric)
            else:
                params.update({"eval_metric": self.eval_metric})

        if feature_weights is not None:
            _deprecated("feature_weights")
        if feature_weights is not None and self.feature_weights is not None:
            _duplicated("feature_weights")
        feature_weights = (
            self.feature_weights
            if self.feature_weights is not None
            else feature_weights
        )

        tree_method = params.get("tree_method", None)
        if self.enable_categorical and tree_method == "exact":
            raise ValueError(
                "Experimental support for categorical data is not implemented for"
                " current tree method yet."
            )
        return model, metric, params, feature_weights

    def _create_dmatrix(self, ref: Optional[DMatrix], **kwargs: Any) -> DMatrix:
        # Use `QuantileDMatrix` to save memory.
        if _can_use_qdm(self.tree_method, self.device) and self.booster != "gblinear":
            try:
                return QuantileDMatrix(
                    **kwargs, ref=ref, nthread=self.n_jobs, max_bin=self.max_bin
                )
            except TypeError:  # `QuantileDMatrix` supports lesser types than DMatrix
                pass
        return DMatrix(**kwargs, nthread=self.n_jobs)

    def _set_evaluation_result(self, evals_result: TrainingCallback.EvalsLog) -> None:
        if evals_result:
            self.evals_result_ = cast(Dict[str, Dict[str, List[float]]], evals_result)

    @_deprecate_positional_args
    def fit(
        self,
        X: ArrayLike,
        y: ArrayLike,
        *,
        sample_weight: Optional[ArrayLike] = None,
        base_margin: Optional[ArrayLike] = None,
        eval_set: Optional[Sequence[Tuple[ArrayLike, ArrayLike]]] = None,
        verbose: Optional[Union[bool, int]] = True,
        xgb_model: Optional[Union[Booster, str, "XGBModel"]] = None,
        sample_weight_eval_set: Optional[Sequence[ArrayLike]] = None,
        base_margin_eval_set: Optional[Sequence[ArrayLike]] = None,
        feature_weights: Optional[ArrayLike] = None,
    ) -> "XGBModel":
        # pylint: disable=invalid-name,attribute-defined-outside-init
        """Fit gradient boosting model.

        Note that calling ``fit()`` multiple times will cause the model object to be
        re-fit from scratch. To resume training from a previous checkpoint, explicitly
        pass ``xgb_model`` argument.

        Parameters
        ----------
        X :
            Input feature matrix. See :ref:`py-data` for a list of supported types.

            When the ``tree_method`` is set to ``hist``, internally, the
            :py:class:`QuantileDMatrix` will be used instead of the :py:class:`DMatrix`
            for conserving memory. However, this has performance implications when the
            device of input data is not matched with algorithm. For instance, if the
            input is a numpy array on CPU but ``cuda`` is used for training, then the
            data is first processed on CPU then transferred to GPU.
        y :
            Labels
        sample_weight :
            instance weights
        base_margin :
            Global bias for each instance. See :doc:`/tutorials/intercept` for details.
        eval_set :
            A list of (X, y) tuple pairs to use as validation sets, for which
            metrics will be computed.
            Validation metrics will help us track the performance of the model.

        verbose :
            If `verbose` is True and an evaluation set is used, the evaluation metric
            measured on the validation set is printed to stdout at each boosting stage.
            If `verbose` is an integer, the evaluation metric is printed at each
            `verbose` boosting stage. The last boosting stage / the boosting stage found
            by using `early_stopping_rounds` is also printed.
        xgb_model :
            file name of stored XGBoost model or 'Booster' instance XGBoost model to be
            loaded before training (allows training continuation).
        sample_weight_eval_set :
            A list of the form [L_1, L_2, ..., L_n], where each L_i is an array like
            object storing instance weights for the i-th validation set.
        base_margin_eval_set :
            A list of the form [M_1, M_2, ..., M_n], where each M_i is an array like
            object storing base margin for the i-th validation set.
        feature_weights :

            .. deprecated:: 3.0.0

            Use `feature_weights` in :py:meth:`__init__` or :py:meth:`set_params`
            instead.

        """
        with config_context(verbosity=self.verbosity):
            params = self.get_xgb_params()
            model, metric, params, feature_weights = self._configure_fit(
                xgb_model, params, feature_weights
            )

            evals_result: TrainingCallback.EvalsLog = {}
            train_dmatrix, evals = _wrap_evaluation_matrices(
                missing=self.missing,
                X=X,
                y=y,
                group=None,
                qid=None,
                sample_weight=sample_weight,
                base_margin=base_margin,
                feature_weights=feature_weights,
                eval_set=eval_set,
                sample_weight_eval_set=sample_weight_eval_set,
                base_margin_eval_set=base_margin_eval_set,
                eval_group=None,
                eval_qid=None,
                create_dmatrix=self._create_dmatrix,
                enable_categorical=self.enable_categorical,
                feature_types=self.feature_types,
            )

            if callable(self.objective):
                obj: Optional[Objective] = _objective_decorator(self.objective)
                params["objective"] = "reg:squarederror"
            else:
                obj = None

            self._Booster = train(
                params,
                train_dmatrix,
                self.get_num_boosting_rounds(),
                evals=evals,
                early_stopping_rounds=self.early_stopping_rounds,
                evals_result=evals_result,
                obj=obj,
                custom_metric=metric,
                verbose_eval=verbose,
                xgb_model=model,
                callbacks=self.callbacks,
            )

            self._set_evaluation_result(evals_result)
            return self

    def _can_use_inplace_predict(self) -> bool:
        if self.booster != "gblinear":
            return True
        return False

    def _get_iteration_range(
        self, iteration_range: Optional[IterationRange]
    ) -> IterationRange:
        if iteration_range is None or iteration_range[1] == 0:
            # Use best_iteration if defined.
            try:
                iteration_range = (0, self.best_iteration + 1)
            except AttributeError:
                iteration_range = (0, 0)
        if self.booster == "gblinear":
            iteration_range = (0, 0)
        return iteration_range

    @_deprecate_positional_args
    def predict(
        self,
        X: ArrayLike,
        *,
        output_margin: bool = False,
        validate_features: bool = True,
        base_margin: Optional[ArrayLike] = None,
        iteration_range: Optional[IterationRange] = None,
    ) -> ArrayLike:
        """Predict with `X`.  If the model is trained with early stopping, then
        :py:attr:`best_iteration` is used automatically. The estimator uses
        `inplace_predict` by default and falls back to using :py:class:`DMatrix` if
        devices between the data and the estimator don't match.

        .. note:: This function is only thread safe for `gbtree` and `dart`.

        Parameters
        ----------
        X :
            Data to predict with. See :ref:`py-data` for a list of supported types.
        output_margin :
            Whether to output the raw untransformed margin value.
        validate_features :
            When this is True, validate that the Booster's and data's feature_names are
            identical.  Otherwise, it is assumed that the feature_names are the same.
        base_margin :
            Global bias for each instance. See :doc:`/tutorials/intercept` for details.
        iteration_range :
            Specifies which layer of trees are used in prediction.  For example, if a
            random forest is trained with 100 rounds.  Specifying ``iteration_range=(10,
            20)``, then only the forests built during [10, 20) (half open set) rounds
            are used in this prediction.

            .. versionadded:: 1.4.0

        Returns
        -------
        prediction

        """
        with config_context(verbosity=self.verbosity):
            iteration_range = self._get_iteration_range(iteration_range)
            if self._can_use_inplace_predict():
                try:
                    predts = self.get_booster().inplace_predict(
                        data=X,
                        iteration_range=iteration_range,
                        predict_type="margin" if output_margin else "value",
                        missing=self.missing,
                        base_margin=base_margin,
                        validate_features=validate_features,
                    )
                    if _is_cupy_alike(predts):
                        cp = import_cupy()

                        predts = cp.asnumpy(predts)  # ensure numpy array is used.
                    return predts
                except TypeError:
                    # coo, csc, dt
                    pass

            test = DMatrix(
                X,
                base_margin=base_margin,
                missing=self.missing,
                nthread=self.n_jobs,
                feature_types=self.feature_types,
                enable_categorical=self.enable_categorical,
            )
            return self.get_booster().predict(
                data=test,
                iteration_range=iteration_range,
                output_margin=output_margin,
                validate_features=validate_features,
            )

    def apply(
        self,
        X: ArrayLike,
        iteration_range: Optional[IterationRange] = None,
    ) -> np.ndarray:
        """Return the predicted leaf every tree for each sample. If the model is trained
        with early stopping, then :py:attr:`best_iteration` is used automatically.

        Parameters
        ----------
        X :
            Input features matrix. See :ref:`py-data` for a list of supported types.

        iteration_range :
            See :py:meth:`predict`.

        Returns
        -------
        X_leaves : array_like, shape=[n_samples, n_trees]
            For each datapoint x in X and for each tree, return the index of the
            leaf x ends up in. Leaves are numbered within
            ``[0; 2**(self.max_depth+1))``, possibly with gaps in the numbering.

        """
        with config_context(verbosity=self.verbosity):
            iteration_range = self._get_iteration_range(iteration_range)
            test_dmatrix = DMatrix(
                X,
                missing=self.missing,
                feature_types=self.feature_types,
                nthread=self.n_jobs,
            )
            return self.get_booster().predict(
                test_dmatrix, pred_leaf=True, iteration_range=iteration_range
            )

    def evals_result(self) -> Dict[str, Dict[str, List[float]]]:
        """Return the evaluation results.

        If **eval_set** is passed to the :py:meth:`fit` function, you can call
        ``evals_result()`` to get evaluation results for all passed **eval_sets**.  When
        **eval_metric** is also passed to the :py:meth:`fit` function, the
        **evals_result** will contain the **eval_metrics** passed to the :py:meth:`fit`
        function.

        The returned evaluation result is a dictionary:

        .. code-block:: python

            {'validation_0': {'logloss': ['0.604835', '0.531479']},
             'validation_1': {'logloss': ['0.41965', '0.17686']}}

        Returns
        -------
        evals_result

        """
        if getattr(self, "evals_result_", None) is not None:
            evals_result = self.evals_result_
        else:
            raise XGBoostError(
                "No evaluation result, `eval_set` is not used during training."
            )

        return evals_result

    @property
    def n_features_in_(self) -> int:
        """Number of features seen during :py:meth:`fit`."""
        booster = self.get_booster()
        return booster.num_features()

    @property
    def feature_names_in_(self) -> np.ndarray:
        """Names of features seen during :py:meth:`fit`.  Defined only when `X` has
        feature names that are all strings.

        """
        feature_names = self.get_booster().feature_names
        if feature_names is None:
            raise AttributeError(
                "`feature_names_in_` is defined only when `X` has feature names that "
                "are all strings."
            )
        return np.array(feature_names)

    @property
    def best_score(self) -> float:
        """The best score obtained by early stopping."""
        return self.get_booster().best_score

    @property
    def best_iteration(self) -> int:
        """The best iteration obtained by early stopping.  This attribute is 0-based,
        for instance if the best iteration is the first round, then best_iteration is 0.

        """
        return self.get_booster().best_iteration

    @property
    def feature_importances_(self) -> np.ndarray:
        """Feature importances property, return depends on `importance_type`
        parameter. When model trained with multi-class/multi-label/multi-target dataset,
        the feature importance is "averaged" over all targets. The "average" is defined
        based on the importance type. For instance, if the importance type is
        "total_gain", then the score is sum of loss change for each split from all
        trees.

        Returns
        -------
        feature_importances_ : array of shape ``[n_features]`` except for multi-class
        linear model, which returns an array with shape `(n_features, n_classes)`

        """
        b: Booster = self.get_booster()

        def dft() -> str:
            return "weight" if self.booster == "gblinear" else "gain"

        score = b.get_score(
            importance_type=self.importance_type if self.importance_type else dft()
        )
        if b.feature_names is None:
            feature_names: FeatureNames = [f"f{i}" for i in range(self.n_features_in_)]
        else:
            feature_names = b.feature_names
        # gblinear returns all features so the `get` in next line is only for gbtree.
        all_features = [score.get(f, 0.0) for f in feature_names]
        all_features_arr = np.array(all_features, dtype=np.float32)
        total = all_features_arr.sum()
        if total == 0:
            return all_features_arr
        return all_features_arr / total

    @property
    def coef_(self) -> np.ndarray:
        """
        Coefficients property

        .. note:: Coefficients are defined only for linear learners

            Coefficients are only defined when the linear model is chosen as
            base learner (`booster=gblinear`). It is not defined for other base
            learner types, such as tree learners (`booster=gbtree`).

        Returns
        -------
        coef_ : array of shape ``[n_features]`` or ``[n_classes, n_features]``
        """
        if self.get_xgb_params()["booster"] != "gblinear":
            raise AttributeError(
                f"Coefficients are not defined for Booster type {self.booster}"
            )
        b = self.get_booster()
        coef = np.array(json.loads(b.get_dump(dump_format="json")[0])["weight"])
        # Logic for multiclass classification
        n_classes = getattr(self, "n_classes_", None)
        if n_classes is not None:
            if n_classes > 2:
                assert len(coef.shape) == 1
                assert coef.shape[0] % n_classes == 0
                coef = coef.reshape((n_classes, -1))
        return coef

    @property
    def intercept_(self) -> np.ndarray:
        """Intercept (bias) property

        For tree-based model, the returned value is the `base_score`.

        Returns
        -------
        intercept_ : array of shape ``(1,)`` or ``[n_classes]``

        """
        booster_config = self.get_xgb_params()["booster"]
        b = self.get_booster()
        if booster_config != "gblinear":  # gbtree, dart
            config = json.loads(b.save_config())
            intercept = config["learner"]["learner_model_param"]["base_score"]
            return np.array([float(intercept)], dtype=np.float32)

        return np.array(
            json.loads(b.get_dump(dump_format="json")[0])["bias"], dtype=np.float32
        )
