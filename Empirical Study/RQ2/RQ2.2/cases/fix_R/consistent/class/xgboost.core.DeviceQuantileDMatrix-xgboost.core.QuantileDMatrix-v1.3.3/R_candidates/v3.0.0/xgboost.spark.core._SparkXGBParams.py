class _SparkXGBParams(
    HasFeaturesCol,
    HasLabelCol,
    HasWeightCol,
    HasPredictionCol,
    HasValidationIndicatorCol,
    HasArbitraryParamsDict,
    HasBaseMarginCol,
    HasFeaturesCols,
    HasEnableSparseDataOptim,
    HasQueryIdCol,
    HasContribPredictionCol,
):
    num_workers = Param(
        Params._dummy(),
        "num_workers",
        "The number of XGBoost workers. Each XGBoost worker corresponds to one spark task.",
        TypeConverters.toInt,
    )
    device = Param(
        Params._dummy(),
        "device",
        (
            "The device type for XGBoost executors. Available options are `cpu`,`cuda`"
            " and `gpu`. Set `device` to `cuda` or `gpu` if the executors are running "
            "on GPU instances. Currently, only one GPU per task is supported."
        ),
        TypeConverters.toString,
    )
    use_gpu = Param(
        Params._dummy(),
        "use_gpu",
        (
            "Deprecated, use `device` instead. A boolean variable. Set use_gpu=true "
            "if the executors are running on GPU instances. Currently, only one GPU per"
            " task is supported."
        ),
        TypeConverters.toBoolean,
    )
    force_repartition = Param(
        Params._dummy(),
        "force_repartition",
        "A boolean variable. Set force_repartition=true if you "
        + "want to force the input dataset to be repartitioned before XGBoost training."
        + "Note: The auto repartitioning judgement is not fully accurate, so it is recommended"
        + "to have force_repartition be True.",
        TypeConverters.toBoolean,
    )
    repartition_random_shuffle = Param(
        Params._dummy(),
        "repartition_random_shuffle",
        "A boolean variable. Set repartition_random_shuffle=true if you want to random shuffle "
        "dataset when repartitioning is required. By default is True.",
        TypeConverters.toBoolean,
    )
    feature_names = Param(
        Params._dummy(),
        "feature_names",
        "A list of str to specify feature names.",
        TypeConverters.toList,
    )
    launch_tracker_on_driver = Param(
        Params._dummy(),
        "launch_tracker_on_driver",
        "A boolean variable. Set launch_tracker_on_driver to true if you want the tracker to be "
        "launched on the driver side; otherwise, it will be launched on the executor side.",
        TypeConverters.toBoolean,
    )
    coll_cfg = Param(
        Params._dummy(),
        "coll_cfg",
        "xgboost.collective.Config. The collective configuration.",
        TypeConverters.identity,
    )

    def set_coll_cfg(self, value: Config) -> "_SparkXGBParams":
        """Set collective configuration"""
        assert isinstance(value, Config)
        self.set(self.coll_cfg, value)
        return self

    def set_device(self, value: str) -> "_SparkXGBParams":
        """Set device, optional value: cpu, cuda, gpu"""
        _check_distributed_params({"device": value})
        assert value in ("cpu", "cuda", "gpu")
        self.set(self.device, value)
        return self

    @classmethod
    def _xgb_cls(cls) -> Type[XGBModel]:
        """
        Subclasses should override this method and
        returns an xgboost.XGBModel subclass
        """
        raise NotImplementedError()

    # Parameters for xgboost.XGBModel()
    @classmethod
    def _get_xgb_params_default(cls) -> Dict[str, Any]:
        """Get the xgboost.sklearn.XGBModel default parameters and filter out some"""
        xgb_model_default = cls._xgb_cls()()
        params_dict = xgb_model_default.get_params()
        filtered_params_dict = {
            k: params_dict[k] for k in params_dict if k not in _unsupported_xgb_params
        }
        filtered_params_dict["n_estimators"] = DEFAULT_N_ESTIMATORS
        return filtered_params_dict

    def _set_xgb_params_default(self) -> None:
        """Set xgboost parameters into spark parameters"""
        filtered_params_dict = self._get_xgb_params_default()
        self._setDefault(**filtered_params_dict)

    def _gen_xgb_params_dict(
        self, gen_xgb_sklearn_estimator_param: bool = False
    ) -> Dict[str, Any]:
        """Generate the xgboost parameters which will be passed into xgboost library"""
        xgb_params = {}
        non_xgb_params = (
            set(_pyspark_specific_params)
            | self._get_fit_params_default().keys()
            | self._get_predict_params_default().keys()
        )
        if not gen_xgb_sklearn_estimator_param:
            non_xgb_params |= set(_non_booster_params)
        for param in self.extractParamMap():
            if param.name not in non_xgb_params:
                xgb_params[param.name] = self.getOrDefault(param)

        arbitrary_params_dict = self.getOrDefault(
            self.getParam("arbitrary_params_dict")
        )
        xgb_params.update(arbitrary_params_dict)
        return xgb_params

    # Parameters for xgboost.XGBModel().fit()
    @classmethod
    def _get_fit_params_default(cls) -> Dict[str, Any]:
        """Get the xgboost.XGBModel().fit() parameters"""
        fit_params = _get_default_params_from_func(
            cls._xgb_cls().fit, _unsupported_fit_params
        )
        return fit_params

    def _set_fit_params_default(self) -> None:
        """Get the xgboost.XGBModel().fit() parameters and set them to spark parameters"""
        filtered_params_dict = self._get_fit_params_default()
        self._setDefault(**filtered_params_dict)

    def _gen_fit_params_dict(self) -> Dict[str, Any]:
        """Generate the fit parameters which will be passed into fit function"""
        fit_params_keys = self._get_fit_params_default().keys()
        fit_params = {}
        for param in self.extractParamMap():
            if param.name in fit_params_keys:
                fit_params[param.name] = self.getOrDefault(param)
        return fit_params

    @classmethod
    def _get_predict_params_default(cls) -> Dict[str, Any]:
        """Get the parameters from xgboost.XGBModel().predict()"""
        predict_params = _get_default_params_from_func(
            cls._xgb_cls().predict, _unsupported_predict_params
        )
        return predict_params

    def _set_predict_params_default(self) -> None:
        """Get the parameters from xgboost.XGBModel().predict() and
        set them into spark parameters"""
        filtered_params_dict = self._get_predict_params_default()
        self._setDefault(**filtered_params_dict)

    def _gen_predict_params_dict(self) -> Dict[str, Any]:
        """Generate predict parameters which will be passed into xgboost.XGBModel().predict()"""
        predict_params_keys = self._get_predict_params_default().keys()
        predict_params = {}
        for param in self.extractParamMap():
            if param.name in predict_params_keys:
                predict_params[param.name] = self.getOrDefault(param)
        return predict_params

    def _validate_gpu_params(
        self, spark_version: str, conf: SparkConf, is_local: bool = False
    ) -> None:
        """Validate the gpu parameters and gpu configurations"""

        if self._run_on_gpu():
            if is_local:
                # Supporting GPU training in Spark local mode is just for debugging
                # purposes, so it's okay for printing the below warning instead of
                # checking the real gpu numbers and raising the exception.
                get_logger(self.__class__.__name__).warning(
                    "You have enabled GPU in spark local mode. Please make sure your"
                    " local node has at least %d GPUs",
                    self.getOrDefault(self.num_workers),
                )
            else:
                executor_gpus = conf.get("spark.executor.resource.gpu.amount")
                if executor_gpus is None:
                    raise ValueError(
                        "The `spark.executor.resource.gpu.amount` is required for training"
                        " on GPU."
                    )
                gpu_per_task = conf.get("spark.task.resource.gpu.amount")
                if gpu_per_task is not None and float(gpu_per_task) > 1.0:
                    get_logger(self.__class__.__name__).warning(
                        "The configuration assigns %s GPUs to each Spark task, but each "
                        "XGBoost training task only utilizes 1 GPU, which will lead to "
                        "unnecessary GPU waste",
                        gpu_per_task,
                    )
                # For 3.5.1+, Spark supports task stage-level scheduling for
                #                          Yarn/K8s/Standalone/Local cluster
                # From 3.4.0 ~ 3.5.0, Spark only supports task stage-level scheduing for
                #                           Standalone/Local cluster
                # For spark below 3.4.0, Task stage-level scheduling is not supported.
                #
                # With stage-level scheduling, spark.task.resource.gpu.amount is not required
                # to be set explicitly. Or else, spark.task.resource.gpu.amount is a must-have and
                # must be set to 1.0
                if spark_version < "3.4.0" or (
                    "3.4.0" <= spark_version < "3.5.1"
                    and not _is_standalone_or_localcluster(conf)
                ):
                    if gpu_per_task is not None:
                        if float(gpu_per_task) < 1.0:
                            raise ValueError(
                                "XGBoost doesn't support GPU fractional configurations. Please set "
                                "`spark.task.resource.gpu.amount=spark.executor.resource.gpu."
                                "amount`. To enable GPU fractional configurations, you can try "
                                "standalone/localcluster with spark 3.4.0+ and"
                                "YARN/K8S with spark 3.5.1+"
                            )
                    else:
                        raise ValueError(
                            "The `spark.task.resource.gpu.amount` is required for training"
                            " on GPU."
                        )

    def _validate_params(self) -> None:
        # pylint: disable=too-many-branches
        init_model = self.getOrDefault("xgb_model")
        if init_model is not None and not isinstance(init_model, Booster):
            raise ValueError(
                "The xgb_model param must be set with a `xgboost.core.Booster` "
                "instance."
            )

        if self.getOrDefault(self.num_workers) < 1:
            raise ValueError(
                f"Number of workers was {self.getOrDefault(self.num_workers)}."
                f"It cannot be less than 1 [Default is 1]"
            )

        tree_method = self.getOrDefault(self.getParam("tree_method"))
        if tree_method == "exact":
            raise ValueError(
                "The `exact` tree method is not supported for distributed systems."
            )

        if self.getOrDefault("objective") is not None:
            if not isinstance(self.getOrDefault("objective"), str):
                raise ValueError("Only string type 'objective' param is allowed.")

        eval_metric = "eval_metric"
        if self.getOrDefault(eval_metric) is not None:
            if not (
                isinstance(self.getOrDefault(eval_metric), str)
                or (
                    isinstance(self.getOrDefault(eval_metric), List)
                    and all(
                        isinstance(metric, str)
                        for metric in self.getOrDefault(eval_metric)
                    )
                )
            ):
                raise ValueError(
                    "Only string type or list of string type 'eval_metric' param is allowed."
                )

        if self.getOrDefault("early_stopping_rounds") is not None:
            if not self._col_is_defined_not_empty(self.validationIndicatorCol):
                raise ValueError(
                    "If 'early_stopping_rounds' param is set, you need to set "
                    "'validation_indicator_col' param as well."
                )

        if self.getOrDefault(self.enable_sparse_data_optim):
            if self.getOrDefault("missing") != 0.0:
                # If DMatrix is constructed from csr / csc matrix, then inactive elements
                # in csr / csc matrix are regarded as missing value, but, in pyspark, we
                # are hard to control elements to be active or inactive in sparse vector column,
                # some spark transformers such as VectorAssembler might compress vectors
                # to be dense or sparse format automatically, and when a spark ML vector object
                # is compressed to sparse vector, then all zero value elements become inactive.
                # So we force setting missing param to be 0 when enable_sparse_data_optim config
                # is True.
                raise ValueError(
                    "If enable_sparse_data_optim is True, missing param != 0 is not supported."
                )
            if self.getOrDefault(self.features_cols):
                raise ValueError(
                    "If enable_sparse_data_optim is True, you cannot set multiple feature columns "
                    "but you should set one feature column with values of "
                    "`pyspark.ml.linalg.Vector` type."
                )

        ss = _get_spark_session()
        sc = ss.sparkContext
        self._validate_gpu_params(ss.version, sc.getConf(), _is_local(sc))

    def _run_on_gpu(self) -> bool:
        """If train or transform on the gpu according to the parameters"""

        return (
            use_cuda(self.getOrDefault(self.device))
            or self.getOrDefault(self.use_gpu)
            or self.getOrDefault(self.getParam("tree_method")) == "gpu_hist"
        )

    def _col_is_defined_not_empty(self, param: "Param[str]") -> bool:
        return self.isDefined(param) and self.getOrDefault(param) != ""
