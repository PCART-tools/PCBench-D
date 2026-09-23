class SparkXGBModelReader(MLReader):
    """
    Spark Xgboost model reader.
    """

    def __init__(self, cls: Type["_SparkXGBModel"]) -> None:
        super().__init__()
        self.cls = cls
        self.logger = get_logger(self.__class__.__name__, level="WARN")

    def load(self, path: str) -> "_SparkXGBModel":
        """
        Load metadata and model for a :py:class:`_SparkXGBModel`

        :return: SparkXGBRegressorModel or SparkXGBClassifierModel instance
        """
        _, py_model = _SparkXGBSharedReadWrite.loadMetadataAndInstance(
            self.cls, path, self.sc, self.logger
        )
        py_model = cast("_SparkXGBModel", py_model)

        xgb_sklearn_params = py_model._gen_xgb_params_dict(
            gen_xgb_sklearn_estimator_param=True
        )
        model_load_path = os.path.join(path, "model")

        ser_xgb_model = "".join(
            _get_spark_session().sparkContext.textFile(model_load_path).collect()
        )

        def create_xgb_model() -> "XGBModel":
            return self.cls._xgb_cls()(**xgb_sklearn_params)

        xgb_model = deserialize_xgb_model(ser_xgb_model, create_xgb_model)
        py_model._xgb_sklearn_model = xgb_model
        return py_model
