class SparkXGBClassifierModel(_ClassificationModel):
    """
    The model returned by :func:`xgboost.spark.SparkXGBClassifier.fit`

    .. Note:: This API is experimental.
    """

    @classmethod
    def _xgb_cls(cls) -> Type[XGBClassifier]:
        return XGBClassifier
