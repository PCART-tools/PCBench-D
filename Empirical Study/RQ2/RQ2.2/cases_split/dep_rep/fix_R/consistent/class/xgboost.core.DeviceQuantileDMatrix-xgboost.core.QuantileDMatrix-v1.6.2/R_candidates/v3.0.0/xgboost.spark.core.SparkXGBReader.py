class SparkXGBReader(MLReader):
    """
    Spark Xgboost estimator reader.
    """

    def __init__(self, cls: Type["_SparkXGBEstimator"]) -> None:
        super().__init__()
        self.cls = cls
        self.logger = get_logger(self.__class__.__name__, level="WARN")

    def load(self, path: str) -> "_SparkXGBEstimator":
        """
        load model.
        """
        _, pyspark_xgb = _SparkXGBSharedReadWrite.loadMetadataAndInstance(
            self.cls, path, self.sc, self.logger
        )
        return cast("_SparkXGBEstimator", pyspark_xgb)
