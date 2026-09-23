class _SparkXGBEstimator(Estimator, _SparkXGBParams, MLReadable, MLWritable):
    _input_kwargs: Dict[str, Any]

    def __init__(self) -> None:
        super().__init__()
        self._set_xgb_params_default()
        self._set_fit_params_default()
        self._set_predict_params_default()
        # Note: The default value for arbitrary_params_dict must always be empty dict.
        #  For additional settings added into "arbitrary_params_dict" by default,
        #  they are added in `setParams`.
        self._setDefault(
            num_workers=1,
            device="cpu",
            use_gpu=False,
            force_repartition=False,
            repartition_random_shuffle=False,
            feature_names=None,
            feature_types=None,
            feature_weights=None,
            arbitrary_params_dict={},
            launch_tracker_on_driver=True,
        )

        self.logger = get_logger(self.__class__.__name__)

    def setParams(self, **kwargs: Any) -> None:  # pylint: disable=invalid-name
        """
        Set params for the estimator.
        """
        _extra_params = {}
        if "arbitrary_params_dict" in kwargs:
            raise ValueError("Invalid param name: 'arbitrary_params_dict'.")

        for k, v in kwargs.items():
            # We're not allowing user use features_cols directly.
            if k == self.features_cols.name:
                raise ValueError(
                    f"Unsupported param '{k}' please use features_col instead."
                )
            if k in _inverse_pyspark_param_alias_map:
                raise ValueError(
                    f"Please use param name {_inverse_pyspark_param_alias_map[k]} instead."
                )
            if k in _pyspark_param_alias_map:
                if k == _inverse_pyspark_param_alias_map[
                    self.featuresCol.name
                ] and isinstance(v, list):
                    real_k = self.features_cols.name
                    k = real_k
                else:
                    real_k = _pyspark_param_alias_map[k]
                    k = real_k

            if self.hasParam(k):
                if k == "features_col" and isinstance(v, list):
                    self._set(**{"features_cols": v})
                else:
                    self._set(**{str(k): v})
            else:
                if (
                    k in _unsupported_xgb_params
                    or k in _unsupported_fit_params
                    or k in _unsupported_predict_params
                    or k in _unsupported_train_params
                ):
                    err_msg = _unsupported_params_hint_message.get(
                        k, f"Unsupported param '{k}'."
                    )
                    raise ValueError(err_msg)
                _extra_params[k] = v

        _check_distributed_params(kwargs)
        _existing_extra_params = self.getOrDefault(self.arbitrary_params_dict)
        self._set(arbitrary_params_dict={**_existing_extra_params, **_extra_params})

    @classmethod
    def _pyspark_model_cls(cls) -> Type["_SparkXGBModel"]:
        """
        Subclasses should override this method and
        returns a _SparkXGBModel subclass
        """
        raise NotImplementedError()

    def _create_pyspark_model(
        self, xgb_model: XGBModel, training_summary: XGBoostTrainingSummary
    ) -> "_SparkXGBModel":
        return self._pyspark_model_cls()(xgb_model, training_summary)

    def _convert_to_sklearn_model(self, booster: bytearray, config: str) -> XGBModel:
        xgb_sklearn_params = self._gen_xgb_params_dict(
            gen_xgb_sklearn_estimator_param=True
        )
        sklearn_model = self._xgb_cls()(**xgb_sklearn_params)
        sklearn_model.load_model(booster)
        sklearn_model._Booster.load_config(config)
        return sklearn_model

    def _repartition_needed(self, dataset: DataFrame) -> bool:
        """
        We repartition the dataset if the number of workers is not equal to the number of
        partitions."""
        if self.getOrDefault(self.force_repartition):
            return True
        num_workers = self.getOrDefault(self.num_workers)
        num_partitions = dataset.rdd.getNumPartitions()
        return not num_workers == num_partitions

    def _get_distributed_train_params(self, dataset: DataFrame) -> Dict[str, Any]:
        """
        This just gets the configuration params for distributed xgboost
        """
        params = self._gen_xgb_params_dict()
        fit_params = self._gen_fit_params_dict()
        verbose_eval = fit_params.pop("verbose", None)

        params.update(fit_params)
        params["verbose_eval"] = verbose_eval
        classification = self._xgb_cls() == XGBClassifier
        if classification:
            num_classes = int(
                dataset.select(countDistinct(alias.label)).collect()[0][0]
            )
            if num_classes <= 2:
                params["objective"] = "binary:logistic"
            else:
                params["objective"] = "multi:softprob"
                params["num_class"] = num_classes
        else:
            # use user specified objective or default objective.
            # e.g., the default objective for Regressor is 'reg:squarederror'
            params["objective"] = self.getOrDefault("objective")

        # TODO: support "num_parallel_tree" for random forest
        params["num_boost_round"] = self.getOrDefault("n_estimators")

        return params

    @classmethod
    def _get_xgb_train_call_args(
        cls, train_params: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        xgb_train_default_args = _get_default_params_from_func(
            worker_train, _unsupported_train_params
        )
        booster_params, kwargs_params = {}, {}
        for key, value in train_params.items():
            if key in xgb_train_default_args:
                kwargs_params[key] = value
            else:
                booster_params[key] = value

        booster_params = {
            k: v for k, v in booster_params.items() if k not in _non_booster_params
        }
        return booster_params, kwargs_params

    def _prepare_input_columns_and_feature_prop(
        self, dataset: DataFrame
    ) -> Tuple[List[Column], FeatureProp]:
        label_col = col(self.getOrDefault(self.labelCol)).alias(alias.label)

        select_cols = [label_col]
        features_cols_names = None
        enable_sparse_data_optim = self.getOrDefault(self.enable_sparse_data_optim)
        if enable_sparse_data_optim:
            features_col_name = self.getOrDefault(self.featuresCol)
            features_col_datatype = dataset.schema[features_col_name].dataType
            if not isinstance(features_col_datatype, VectorUDT):
                raise ValueError(
                    "If enable_sparse_data_optim is True, the feature column values must be "
                    "`pyspark.ml.linalg.Vector` type."
                )
            select_cols.extend(_get_unwrapped_vec_cols(col(features_col_name)))
        else:
            if self.getOrDefault(self.features_cols):
                features_cols_names = self.getOrDefault(self.features_cols)
                features_cols = _validate_and_convert_feature_col_as_float_col_list(
                    dataset, features_cols_names
                )
                select_cols.extend(features_cols)
            else:
                features_array_col = _validate_and_convert_feature_col_as_array_col(
                    dataset, self.getOrDefault(self.featuresCol)
                )
                select_cols.append(features_array_col)

        if self._col_is_defined_not_empty(self.weightCol):
            select_cols.append(
                col(self.getOrDefault(self.weightCol)).alias(alias.weight)
            )

        has_validation_col = False
        if self._col_is_defined_not_empty(self.validationIndicatorCol):
            select_cols.append(
                col(self.getOrDefault(self.validationIndicatorCol)).alias(alias.valid)
            )
            # In some cases, see https://issues.apache.org/jira/browse/SPARK-40407,
            # the df.repartition can result in some reducer partitions without data,
            # which will cause exception or hanging issue when creating DMatrix.
            has_validation_col = True

        if self._col_is_defined_not_empty(self.base_margin_col):
            select_cols.append(
                col(self.getOrDefault(self.base_margin_col)).alias(alias.margin)
            )

        if self._col_is_defined_not_empty(self.qid_col):
            select_cols.append(col(self.getOrDefault(self.qid_col)).alias(alias.qid))

        feature_prop = FeatureProp(
            enable_sparse_data_optim, has_validation_col, features_cols_names
        )
        return select_cols, feature_prop

    def _prepare_input(self, dataset: DataFrame) -> Tuple[DataFrame, FeatureProp]:
        """Prepare the input including column pruning, repartition and so on"""

        select_cols, feature_prop = self._prepare_input_columns_and_feature_prop(
            dataset
        )

        dataset = dataset.select(*select_cols)

        num_workers = self.getOrDefault(self.num_workers)
        sc = _get_spark_session().sparkContext
        max_concurrent_tasks = _get_max_num_concurrent_tasks(sc)

        if num_workers > max_concurrent_tasks:
            get_logger(self.__class__.__name__).warning(
                "The num_workers %s set for xgboost distributed "
                "training is greater than current max number of concurrent "
                "spark task slots, you need wait until more task slots available "
                "or you need increase spark cluster workers.",
                num_workers,
            )

        if self._repartition_needed(dataset):
            if self._col_is_defined_not_empty(self.qid_col):
                # For ranking problem, we need to try best the put the instances with
                # same group into the same partition
                dataset = dataset.repartitionByRange(num_workers, alias.qid)
            else:
                # If validationIndicatorCol defined, and if user unionise train and validation
                # dataset, users must set force_repartition to true to force repartition.
                # Or else some partitions might contain only train or validation dataset.
                if self.getOrDefault(self.repartition_random_shuffle):
                    # In some cases, spark round-robin repartition might cause data skew
                    # use random shuffle can address it.
                    dataset = dataset.repartition(num_workers, rand(1))
                else:
                    dataset = dataset.repartition(num_workers)

        if self._col_is_defined_not_empty(self.qid_col):
            # XGBoost requires qid to be sorted for each partition
            dataset = dataset.sortWithinPartitions(alias.qid, ascending=True)

        return dataset, feature_prop

    def _get_xgb_parameters(
        self, dataset: DataFrame
    ) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
        train_params = self._get_distributed_train_params(dataset)
        booster_params, train_call_kwargs_params = self._get_xgb_train_call_args(
            train_params
        )
        cpu_per_task = int(
            _get_spark_session().sparkContext.getConf().get("spark.task.cpus", "1")
        )

        dmatrix_kwargs = {
            "nthread": cpu_per_task,
            "feature_types": self.getOrDefault("feature_types"),
            "feature_names": self.getOrDefault("feature_names"),
            "feature_weights": self.getOrDefault("feature_weights"),
            "missing": float(self.getOrDefault("missing")),
        }
        if dmatrix_kwargs["feature_types"] is not None:
            dmatrix_kwargs["enable_categorical"] = True
        booster_params["nthread"] = cpu_per_task

        # Remove the parameters whose value is None
        booster_params = {k: v for k, v in booster_params.items() if v is not None}
        train_call_kwargs_params = {
            k: v for k, v in train_call_kwargs_params.items() if v is not None
        }
        dmatrix_kwargs = {k: v for k, v in dmatrix_kwargs.items() if v is not None}

        return booster_params, train_call_kwargs_params, dmatrix_kwargs

    def _skip_stage_level_scheduling(self, spark_version: str, conf: SparkConf) -> bool:
        # pylint: disable=too-many-return-statements
        """Check if stage-level scheduling is not needed,
        return true to skip stage-level scheduling"""

        if self._run_on_gpu():
            if spark_version < "3.4.0":
                self.logger.info(
                    "Stage-level scheduling in xgboost requires spark version 3.4.0+"
                )
                return True

            if (
                "3.4.0" <= spark_version < "3.5.1"
                and not _is_standalone_or_localcluster(conf)
            ):
                self.logger.info(
                    "For %s, Stage-level scheduling in xgboost requires spark standalone "
                    "or local-cluster mode",
                    spark_version,
                )
                return True

            executor_cores = conf.get("spark.executor.cores")
            executor_gpus = conf.get("spark.executor.resource.gpu.amount")
            if executor_cores is None or executor_gpus is None:
                self.logger.info(
                    "Stage-level scheduling in xgboost requires spark.executor.cores, "
                    "spark.executor.resource.gpu.amount to be set."
                )
                return True

            if int(executor_cores) == 1:
                # there will be only 1 task running at any time.
                self.logger.info(
                    "Stage-level scheduling in xgboost requires spark.executor.cores > 1 "
                )
                return True

            if int(executor_gpus) > 1:
                # For spark.executor.resource.gpu.amount > 1, we suppose user knows how to configure
                # to make xgboost run successfully.
                #
                self.logger.info(
                    "Stage-level scheduling in xgboost will not work "
                    "when spark.executor.resource.gpu.amount>1"
                )
                return True

            task_gpu_amount = conf.get("spark.task.resource.gpu.amount")

            if task_gpu_amount is None:
                # The ETL tasks will not grab a gpu when spark.task.resource.gpu.amount is not set,
                # but with stage-level scheduling, we can make training task grab the gpu.
                return False

            if float(task_gpu_amount) == float(executor_gpus):
                # spark.executor.resource.gpu.amount=spark.task.resource.gpu.amount "
                # results in only 1 task running at a time, which may cause perf issue.
                return True

            # We can enable stage-level scheduling
            return False

        # CPU training doesn't require stage-level scheduling
        return True

    def _try_stage_level_scheduling(self, rdd: RDD) -> RDD:
        """Try to enable stage-level scheduling"""
        ss = _get_spark_session()
        conf = ss.sparkContext.getConf()
        if _is_local(ss.sparkContext) or self._skip_stage_level_scheduling(
            ss.version, conf
        ):
            return rdd

        # executor_cores will not be None
        executor_cores = conf.get("spark.executor.cores")
        assert executor_cores is not None

        # Spark-rapids is a project to leverage GPUs to accelerate spark SQL.
        # If spark-rapids is enabled, to avoid GPU OOM, we don't allow other
        # ETL gpu tasks running alongside training tasks.
        spark_plugins = ss.conf.get("spark.plugins", " ")
        assert spark_plugins is not None
        spark_rapids_sql_enabled = ss.conf.get("spark.rapids.sql.enabled", "true")
        assert spark_rapids_sql_enabled is not None

        task_cores = (
            int(executor_cores)
            if "com.nvidia.spark.SQLPlugin" in spark_plugins
            and "true" == spark_rapids_sql_enabled.lower()
            else (int(executor_cores) // 2) + 1
        )

        # Each training task requires cpu cores > total executor cores//2 + 1 which can
        # make sure the tasks be sent to different executors.
        #
        # Please note that we can't use GPU to limit the concurrent tasks because of
        # https://issues.apache.org/jira/browse/SPARK-45527.

        task_gpus = 1.0
        treqs = TaskResourceRequests().cpus(task_cores).resource("gpu", task_gpus)
        rp = ResourceProfileBuilder().require(treqs).build

        self.logger.info(
            "XGBoost training tasks require the resource(cores=%s, gpu=%s).",
            task_cores,
            task_gpus,
        )
        return rdd.withResources(rp)

    def _get_tracker_args(self) -> Tuple[bool, Dict[str, Any]]:
        """Start the tracker and return the tracker envs on the driver side"""
        launch_tracker_on_driver = self.getOrDefault(self.launch_tracker_on_driver)
        rabit_args = {}
        if launch_tracker_on_driver:
            conf = Config()
            if self.isDefined(self.coll_cfg):
                conf = self.getOrDefault(self.coll_cfg)
                assert isinstance(conf, Config)

            if conf.tracker_host_ip is None:
                conf.tracker_host_ip = (
                    _get_spark_session().sparkContext.getConf().get("spark.driver.host")
                )
            num_workers = self.getOrDefault(self.num_workers)
            rabit_args.update(_get_rabit_args(conf, num_workers))
        else:
            if self.isDefined(self.coll_cfg):
                conf = self.getOrDefault(self.coll_cfg)
                assert isinstance(conf, Config)
                if conf.tracker_host_ip is not None:
                    raise ValueError(
                        f"You must enable launch_tracker_on_driver to use "
                        f"tracker host: {conf.tracker_host_ip}"
                    )
        return launch_tracker_on_driver, rabit_args

    def _fit(self, dataset: DataFrame) -> "_SparkXGBModel":
        # pylint: disable=too-many-statements, too-many-locals
        self._validate_params()

        dataset, feature_prop = self._prepare_input(dataset)

        (
            booster_params,
            train_call_kwargs_params,
            dmatrix_kwargs,
        ) = self._get_xgb_parameters(dataset)

        run_on_gpu = self._run_on_gpu()

        is_local = _is_local(_get_spark_session().sparkContext)

        num_workers = self.getOrDefault(self.num_workers)

        launch_tracker_on_driver, rabit_args = self._get_tracker_args()
        conf: Optional[Config] = (
            self.getOrDefault(self.coll_cfg) if self.isSet(self.coll_cfg) else None
        )

        log_level = get_logger_level(_LOG_TAG)

        use_rmm = get_config()["use_rmm"]

        def _train_booster(
            pandas_df_iter: Iterator[pd.DataFrame],
        ) -> Iterator[pd.DataFrame]:
            """Takes in an RDD partition and outputs a booster for that partition after
            going through the Rabit Ring protocol

            """
            from pyspark import BarrierTaskContext

            context = BarrierTaskContext.get()
            context.barrier()

            dev_ordinal = None
            use_qdm = _can_use_qdm(
                booster_params.get("tree_method", None),
                booster_params.get("device", None),
            )
            verbosity = booster_params.get("verbosity", 1)
            msg = "Training on CPUs"
            if run_on_gpu:
                dev_ordinal = (
                    context.partitionId() if is_local else _get_gpu_id(context)
                )
                booster_params["device"] = "cuda:" + str(dev_ordinal)
                # If cuDF is not installed, then using DMatrix instead of QDM,
                # because without cuDF, DMatrix performs better than QDM.
                # Note: Checking `is_cudf_available` in spark worker side because
                # spark worker might has different python environment with driver side.
                use_qdm = use_qdm and is_cudf_available()
                msg = (
                    f"Leveraging {booster_params['device']} to train with "
                    f"QDM: {'on' if use_qdm else 'off'}"
                )

            if use_qdm and (booster_params.get("max_bin", None) is not None):
                dmatrix_kwargs["max_bin"] = booster_params["max_bin"]
            _rabit_args = rabit_args
            if context.partitionId() == 0:
                if not launch_tracker_on_driver:
                    _conf = conf if conf is not None else Config()
                    _conf.tracker_host_ip = _get_host_ip(context)
                    _rabit_args = _get_rabit_args(_conf, num_workers)
                get_logger(_LOG_TAG, log_level).info(msg)

            worker_message: Dict[str, Any] = {
                "use_qdm": use_qdm,
            }

            if not launch_tracker_on_driver:
                worker_message["rabit_msg"] = _rabit_args

            messages = context.allGather(message=json.dumps(worker_message))
            if len(set(json.loads(x)["use_qdm"] for x in messages)) != 1:
                raise RuntimeError("The workers' cudf environments are in-consistent ")

            if not launch_tracker_on_driver:
                _rabit_args = json.loads(messages[0])["rabit_msg"]

            evals_result: Dict[str, Any] = {}
            with config_context(
                verbosity=verbosity, use_rmm=use_rmm
            ), CommunicatorContext(context, **_rabit_args):
                dtrain, dvalid = create_dmatrix_from_partitions(
                    iterator=pandas_df_iter,
                    feature_cols=feature_prop.features_cols_names,
                    dev_ordinal=dev_ordinal,
                    use_qdm=use_qdm,
                    kwargs=dmatrix_kwargs,
                    enable_sparse_data_optim=feature_prop.enable_sparse_data_optim,
                    has_validation_col=feature_prop.has_validation_col,
                )
                if dvalid is not None:
                    dval = [(dtrain, "training"), (dvalid, "validation")]
                else:
                    dval = [(dtrain, "training")]
                booster = worker_train(
                    params=booster_params,
                    dtrain=dtrain,
                    evals=dval,
                    evals_result=evals_result,
                    **train_call_kwargs_params,
                )
            context.barrier()

            if context.partitionId() == 0:
                yield pd.DataFrame({"data": [json.dumps(dict(evals_result))]})
                config = booster.save_config()
                yield pd.DataFrame({"data": [config]})
                booster_json = booster.save_raw("json").decode("utf-8")

                for offset in range(0, len(booster_json), _MODEL_CHUNK_SIZE):
                    booster_chunk = booster_json[offset : offset + _MODEL_CHUNK_SIZE]
                    yield pd.DataFrame({"data": [booster_chunk]})

        def _run_job() -> Tuple[str, str, str]:
            rdd = (
                dataset.mapInPandas(
                    _train_booster,  # type: ignore
                    schema="data string",
                )
                .rdd.barrier()
                .mapPartitions(lambda x: x)
            )
            rdd_with_resource = self._try_stage_level_scheduling(rdd)
            ret = rdd_with_resource.collect()
            data = [v[0] for v in ret]
            return data[0], data[1], "".join(data[2:])

        get_logger(_LOG_TAG).info(
            "Running xgboost-%s on %s workers with"
            "\n\tbooster params: %s"
            "\n\ttrain_call_kwargs_params: %s"
            "\n\tdmatrix_kwargs: %s",
            _py_version(),
            num_workers,
            booster_params,
            train_call_kwargs_params,
            dmatrix_kwargs,
        )
        (evals_result, config, booster) = _run_job()
        get_logger(_LOG_TAG).info("Finished xgboost training!")

        result_xgb_model = self._convert_to_sklearn_model(
            bytearray(booster, "utf-8"), config
        )
        training_summary = XGBoostTrainingSummary.from_metrics(json.loads(evals_result))
        spark_model = self._create_pyspark_model(result_xgb_model, training_summary)
        # According to pyspark ML convention, the model uid should be the same
        # with estimator uid.
        spark_model._resetUid(self.uid)
        return self._copyValues(spark_model)

    def write(self) -> "SparkXGBWriter":
        """
        Return the writer for saving the estimator.
        """
        return SparkXGBWriter(self)

    @classmethod
    def read(cls) -> "SparkXGBReader":
        """
        Return the reader for loading the estimator.
        """
        return SparkXGBReader(cls)
