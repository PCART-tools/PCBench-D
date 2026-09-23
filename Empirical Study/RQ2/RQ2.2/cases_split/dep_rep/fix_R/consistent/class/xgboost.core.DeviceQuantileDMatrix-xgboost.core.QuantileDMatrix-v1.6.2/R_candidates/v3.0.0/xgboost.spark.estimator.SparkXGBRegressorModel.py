class SparkXGBRegressorModel(_SparkXGBModel):
    """
    The model returned by :func:`xgboost.spark.SparkXGBRegressor.fit`

    .. Note:: This API is experimental.
    """

    @classmethod
    def _xgb_cls(cls) -> Type[XGBRegressor]:
        return XGBRegressor
