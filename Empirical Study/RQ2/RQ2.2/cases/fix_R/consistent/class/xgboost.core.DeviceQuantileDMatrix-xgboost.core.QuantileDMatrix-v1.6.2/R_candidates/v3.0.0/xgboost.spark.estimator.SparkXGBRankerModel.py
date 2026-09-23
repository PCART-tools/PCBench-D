class SparkXGBRankerModel(_SparkXGBModel):
    """
    The model returned by :func:`xgboost.spark.SparkXGBRanker.fit`

    .. Note:: This API is experimental.
    """

    @classmethod
    def _xgb_cls(cls) -> Type[XGBRanker]:
        return XGBRanker
