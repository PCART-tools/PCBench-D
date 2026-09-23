class SparkXGBWriter(MLWriter):
    """
    Spark Xgboost estimator writer.
    """

    def __init__(self, instance: "_SparkXGBEstimator") -> None:
        super().__init__()
        self.instance = instance
        self.logger = get_logger(self.__class__.__name__, level="WARN")

    def saveImpl(self, path: str) -> None:
        """
        save model.
        """
        _SparkXGBSharedReadWrite.saveMetadata(self.instance, path, self.sc, self.logger)
