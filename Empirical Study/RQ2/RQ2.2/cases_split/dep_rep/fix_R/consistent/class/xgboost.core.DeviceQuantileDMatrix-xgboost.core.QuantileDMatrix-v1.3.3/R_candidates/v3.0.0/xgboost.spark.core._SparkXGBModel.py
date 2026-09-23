class _SparkXGBModel(Model, _SparkXGBParams, MLReadable, MLWritable):
    def __init__(
        self,
        xgb_sklearn_model: Optional[XGBModel] = None,
        training_summary: Optional[XGBoostTrainingSummary] = None,
    ) -> None:
        super().__init__()
        self._xgb_sklearn_model = xgb_sklearn_model
        self.training_summary = training_summary

    @classmethod
    def _xgb_cls(cls) -> Type[XGBModel]:
        raise NotImplementedError()

    def get_booster(self) -> Booster:
        """
        Return the `xgboost.core.Booster` instance.
        """
        assert self._xgb_sklearn_model is not None
        return self._xgb_sklearn_model.get_booster()

    def get_feature_importances(
        self, importance_type: str = "weight"
    ) -> Dict[str, Union[float, List[float]]]:
        """Get feature importance of each feature.
        Importance type can be defined as:

        * 'weight': the number of times a feature is used to split the data across all trees.
        * 'gain': the average gain across all splits the feature is used in.
        * 'cover': the average coverage across all splits the feature is used in.
        * 'total_gain': the total gain across all splits the feature is used in.
        * 'total_cover': the total coverage across all splits the feature is used in.

        Parameters
        ----------
        importance_type: str, default 'weight'
            One of the importance types defined above.
        """
        return self.get_booster().get_score(importance_type=importance_type)

    def write(self) -> "SparkXGBModelWriter":
        """
        Return the writer for saving the model.
        """
        return SparkXGBModelWriter(self)

    @classmethod
    def read(cls) -> "SparkXGBModelReader":
        """
        Return the reader for loading the model.
        """
        return SparkXGBModelReader(cls)

    def _get_feature_col(
        self, dataset: DataFrame
    ) -> Tuple[List[Column], Optional[List[str]]]:
        """XGBoost model trained with features_cols parameter can also predict
        vector or array feature type. But first we need to check features_cols
        and then featuresCol
        """
        if self.getOrDefault(self.enable_sparse_data_optim):
            feature_col_names = None
            features_col = _get_unwrapped_vec_cols(
                col(self.getOrDefault(self.featuresCol))
            )
            return features_col, feature_col_names

        feature_col_names = self.getOrDefault(self.features_cols)
        features_col = []
        if feature_col_names and set(feature_col_names).issubset(set(dataset.columns)):
            # The model is trained with features_cols and the predicted dataset
            # also contains all the columns specified by features_cols.
            features_col = _validate_and_convert_feature_col_as_float_col_list(
                dataset, feature_col_names
            )
        else:
            # 1. The model was trained by features_cols, but the dataset doesn't contain
            #       all the columns specified by features_cols, so we need to check if
            #       the dataframe has the featuresCol
            # 2. The model was trained by featuresCol, and the predicted dataset must contain
            #       featuresCol column.
            feature_col_names = None
            features_col.append(
                _validate_and_convert_feature_col_as_array_col(
                    dataset, self.getOrDefault(self.featuresCol)
                )
            )
        return features_col, feature_col_names

    def _get_pred_contrib_col_name(self) -> Optional[str]:
        """Return the pred_contrib_col col name"""
        pred_contrib_col_name = None
        if self._col_is_defined_not_empty(self.pred_contrib_col):
            pred_contrib_col_name = self.getOrDefault(self.pred_contrib_col)

        return pred_contrib_col_name

    def _out_schema(self) -> Tuple[bool, str]:
        """Return the bool to indicate if it's a single prediction, true is single prediction,
        and the returned type of the user-defined function. The value must
        be a DDL-formatted type string."""

        if self._get_pred_contrib_col_name() is not None:
            return False, f"{pred.prediction} double, {pred.pred_contrib} array<double>"

        return True, "double"

    def _get_predict_func(self) -> Callable:
        """Return the true prediction function which will be running on the executor side"""

        predict_params = self._gen_predict_params_dict()
        pred_contrib_col_name = self._get_pred_contrib_col_name()

        def _predict(
            model: XGBModel, X: ArrayLike, base_margin: Optional[ArrayLike]
        ) -> Union[pd.DataFrame, pd.Series]:
            data = {}
            preds = model.predict(
                X,
                base_margin=base_margin,
                validate_features=False,
                **predict_params,
            )
            data[pred.prediction] = pd.Series(preds)

            if pred_contrib_col_name is not None:
                contribs = pred_contribs(model, X, base_margin)
                data[pred.pred_contrib] = pd.Series(list(contribs))
                return pd.DataFrame(data=data)

            return data[pred.prediction]

        return _predict

    def _post_transform(self, dataset: DataFrame, pred_col: Column) -> DataFrame:
        """Post process of transform"""
        prediction_col_name = self.getOrDefault(self.predictionCol)
        single_pred, _ = self._out_schema()

        if single_pred:
            if prediction_col_name:
                dataset = dataset.withColumn(prediction_col_name, pred_col)
        else:
            pred_struct_col = "_prediction_struct"
            dataset = dataset.withColumn(pred_struct_col, pred_col)

            if prediction_col_name:
                dataset = dataset.withColumn(
                    prediction_col_name, getattr(col(pred_struct_col), pred.prediction)
                )

            pred_contrib_col_name = self._get_pred_contrib_col_name()
            if pred_contrib_col_name is not None:
                dataset = dataset.withColumn(
                    pred_contrib_col_name,
                    array_to_vector(getattr(col(pred_struct_col), pred.pred_contrib)),
                )

            dataset = dataset.drop(pred_struct_col)
        return dataset

    def _run_on_gpu(self) -> bool:
        """If gpu is used to do the prediction according to the parameters
        and spark configurations"""

        use_gpu_by_params = super()._run_on_gpu()

        if _is_local(_get_spark_session().sparkContext):
            # if it's local model, no need to check the spark configurations
            return use_gpu_by_params

        gpu_per_task = (
            _get_spark_session()
            .sparkContext.getConf()
            .get("spark.task.resource.gpu.amount")
        )

        # User don't set gpu configurations, just use cpu
        if gpu_per_task is None:
            if use_gpu_by_params:
                get_logger(_LOG_TAG).warning(
                    "Do the prediction on the CPUs since "
                    "no gpu configurations are set"
                )
            return False

        # User already sets the gpu configurations.
        return use_gpu_by_params

    def _transform(self, dataset: DataFrame) -> DataFrame:
        # pylint: disable=too-many-statements, too-many-locals
        # Save xgb_sklearn_model and predict_params to be local variable
        # to avoid the `self` object to be pickled to remote.
        xgb_sklearn_model = self._xgb_sklearn_model

        base_margin_col = None
        if self._col_is_defined_not_empty(self.base_margin_col):
            base_margin_col = col(self.getOrDefault(self.base_margin_col)).alias(
                alias.margin
            )
        has_base_margin = base_margin_col is not None

        features_col, feature_col_names = self._get_feature_col(dataset)
        enable_sparse_data_optim = self.getOrDefault(self.enable_sparse_data_optim)

        predict_func = self._get_predict_func()

        _, schema = self._out_schema()

        is_local = _is_local(_get_spark_session().sparkContext)
        run_on_gpu = self._run_on_gpu()

        log_level = get_logger_level(_LOG_TAG)

        @pandas_udf(schema)  # type: ignore
        def predict_udf(iterator: Iterator[pd.DataFrame]) -> Iterator[pd.Series]:
            assert xgb_sklearn_model is not None
            model = xgb_sklearn_model

            from pyspark import TaskContext

            context = TaskContext.get()
            assert context is not None

            dev_ordinal = -1

            msg = "Do the inference on the CPUs"
            if run_on_gpu:
                if is_cudf_available() and is_cupy_available():
                    if is_local:
                        cp = import_cupy()

                        total_gpus = cp.cuda.runtime.getDeviceCount()
                        if total_gpus > 0:
                            partition_id = context.partitionId()
                            # For transform local mode, default the dev_ordinal to
                            # (partition id) % gpus.
                            dev_ordinal = partition_id % total_gpus
                    else:
                        dev_ordinal = _get_gpu_id(context)

                    if dev_ordinal >= 0:
                        device = "cuda:" + str(dev_ordinal)
                        msg = "Do the inference with device: " + device
                        model.set_params(device=device)
                    else:
                        msg = "Couldn't get the correct gpu id, fallback the inference on the CPUs"
                else:
                    msg = "CUDF or Cupy is unavailable, fallback the inference on the CPUs"

            if context.partitionId() == 0:
                get_logger(_LOG_TAG, log_level).info(msg)

            def to_gpu_if_possible(data: ArrayLike) -> ArrayLike:
                """Move the data to gpu if possible"""
                if dev_ordinal >= 0:
                    import cudf
                    import cupy as cp

                    # We must set the device after import cudf, which will change the device id to 0
                    # See https://github.com/rapidsai/cudf/issues/11386
                    cp.cuda.runtime.setDevice(dev_ordinal)  # pylint: disable=I1101
                    df = cudf.DataFrame(data)
                    del data
                    return df
                return data

            for data in iterator:
                if enable_sparse_data_optim:
                    X = _read_csr_matrix_from_unwrapped_spark_vec(data)
                else:
                    if feature_col_names is not None:
                        tmp: ArrayLike = data[feature_col_names]
                    else:
                        tmp = stack_series(data[alias.data])
                    X = to_gpu_if_possible(tmp)

                if has_base_margin:
                    base_margin = to_gpu_if_possible(data[alias.margin])
                else:
                    base_margin = None

                yield predict_func(model, X, base_margin)

        if has_base_margin:
            assert base_margin_col is not None
            pred_col = predict_udf(struct(*features_col, base_margin_col))
        else:
            pred_col = predict_udf(struct(*features_col))

        return self._post_transform(dataset, pred_col)
