class SparkXGBModelWriter(MLWriter):
    """
    Spark Xgboost model writer.
    """

    def __init__(self, instance: _SparkXGBModel) -> None:
        super().__init__()
        self.instance = instance
        self.logger = get_logger(self.__class__.__name__, level="WARN")

    def saveImpl(self, path: str) -> None:
        """
        Save metadata and model for a :py:class:`_SparkXGBModel`
        - save metadata to path/metadata
        - save model to path/model.json
        """
        xgb_model = self.instance._xgb_sklearn_model
        assert xgb_model is not None
        _SparkXGBSharedReadWrite.saveMetadata(self.instance, path, self.sc, self.logger)
        model_save_path = os.path.join(path, "model")
        booster = xgb_model.get_booster().save_raw("json").decode("utf-8")
        booster_chunks = []

        for offset in range(0, len(booster), _MODEL_CHUNK_SIZE):
            booster_chunks.append(booster[offset : offset + _MODEL_CHUNK_SIZE])

        _get_spark_session().sparkContext.parallelize(booster_chunks, 1).saveAsTextFile(
            model_save_path
        )
