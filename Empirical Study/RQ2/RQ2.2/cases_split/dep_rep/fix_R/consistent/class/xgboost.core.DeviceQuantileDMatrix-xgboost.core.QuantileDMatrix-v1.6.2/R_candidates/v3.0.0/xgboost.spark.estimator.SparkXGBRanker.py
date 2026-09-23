class SparkXGBRanker(_SparkXGBEstimator):
    """SparkXGBRanker is a PySpark ML estimator. It implements the XGBoost
    ranking algorithm based on XGBoost python library, and it can be used in
    PySpark Pipeline and PySpark ML meta algorithms like
    :py:class:`~pyspark.ml.tuning.CrossValidator`/
    :py:class:`~pyspark.ml.tuning.TrainValidationSplit`/
    :py:class:`~pyspark.ml.classification.OneVsRest`

    SparkXGBRanker automatically supports most of the parameters in
    :py:class:`xgboost.XGBRanker` constructor and most of the parameters used in
    :py:meth:`xgboost.XGBRanker.fit` and :py:meth:`xgboost.XGBRanker.predict` method.

    To enable GPU support, set `device` to `cuda` or `gpu`.

    SparkXGBRanker doesn't support setting `base_margin` explicitly as well, but support
    another param called `base_margin_col`. see doc below for more details.

    SparkXGBRanker doesn't support setting `output_margin`, but we can get output margin
    from the raw prediction column. See `raw_prediction_col` param doc below for more
    details.

    SparkXGBRanker doesn't support `validate_features` and `output_margin` param.

    SparkXGBRanker doesn't support setting `nthread` xgboost param, instead, the
    `nthread` param for each xgboost worker will be set equal to `spark.task.cpus`
    config value.


    Parameters
    ----------

    features_col:
        When the value is string, it requires the features column name to be vector type.
        When the value is a list of string, it requires all the feature columns to be numeric types.
    label_col:
        Label column name. Default to "label".
    prediction_col:
        Prediction column name. Default to "prediction"
    pred_contrib_col:
        Contribution prediction column name.
    validation_indicator_col:
        For params related to `xgboost.XGBRanker` training with
        evaluation dataset's supervision,
        set :py:attr:`xgboost.spark.SparkXGBRanker.validation_indicator_col`
        parameter instead of setting the `eval_set` parameter in :py:class:`xgboost.XGBRanker`
        fit method.
    weight_col:
        To specify the weight of the training and validation dataset, set
        :py:attr:`xgboost.spark.SparkXGBRanker.weight_col` parameter instead of setting
        `sample_weight` and `sample_weight_eval_set` parameter in :py:class:`xgboost.XGBRanker`
        fit method.
    base_margin_col:
        To specify the base margins of the training and validation
        dataset, set :py:attr:`xgboost.spark.SparkXGBRanker.base_margin_col` parameter
        instead of setting `base_margin` and `base_margin_eval_set` in the
        :py:class:`xgboost.XGBRanker` fit method.
    qid_col:
        Query id column name.
    num_workers:
        How many XGBoost workers to be used to train.
        Each XGBoost worker corresponds to one spark task.
    use_gpu:
        .. deprecated:: 2.0.0

        Use `device` instead.

    device:

        .. versionadded:: 2.0.0

        Device for XGBoost workers, available options are `cpu`, `cuda`, and `gpu`.

    force_repartition:
        Boolean value to specify if forcing the input dataset to be repartitioned
        before XGBoost training.
    repartition_random_shuffle:
        Boolean value to specify if randomly shuffling the dataset when repartitioning is required.
    enable_sparse_data_optim:
        Boolean value to specify if enabling sparse data optimization, if True,
        Xgboost DMatrix object will be constructed from sparse matrix instead of
        dense matrix.
    launch_tracker_on_driver:
        Boolean value to indicate whether the tracker should be launched on the driver side or
        the executor side.
    coll_cfg:
        The collective configuration. See :py:class:`~xgboost.collective.Config`

    kwargs:
        A dictionary of xgboost parameters, please refer to
        https://xgboost.readthedocs.io/en/stable/parameter.html

    .. Note:: The Parameters chart above contains parameters that need special handling.
        For a full list of parameters, see entries with `Param(parent=...` below.

    .. Note:: This API is experimental.

    Examples
    --------

    >>> from xgboost.spark import SparkXGBRanker
    >>> from pyspark.ml.linalg import Vectors
    >>> ranker = SparkXGBRanker(qid_col="qid")
    >>> df_train = spark.createDataFrame(
    ...     [
    ...         (Vectors.dense(1.0, 2.0, 3.0), 0, 0),
    ...         (Vectors.dense(4.0, 5.0, 6.0), 1, 0),
    ...         (Vectors.dense(9.0, 4.0, 8.0), 2, 0),
    ...         (Vectors.sparse(3, {1: 1.0, 2: 5.5}), 0, 1),
    ...         (Vectors.sparse(3, {1: 6.0, 2: 7.5}), 1, 1),
    ...         (Vectors.sparse(3, {1: 8.0, 2: 9.5}), 2, 1),
    ...     ],
    ...     ["features", "label", "qid"],
    ... )
    >>> df_test = spark.createDataFrame(
    ...     [
    ...         (Vectors.dense(1.5, 2.0, 3.0), 0),
    ...         (Vectors.dense(4.5, 5.0, 6.0), 0),
    ...         (Vectors.dense(9.0, 4.5, 8.0), 0),
    ...         (Vectors.sparse(3, {1: 1.0, 2: 6.0}), 1),
    ...         (Vectors.sparse(3, {1: 6.0, 2: 7.0}), 1),
    ...         (Vectors.sparse(3, {1: 8.0, 2: 10.5}), 1),
    ...     ],
    ...     ["features", "qid"],
    ... )
    >>> model = ranker.fit(df_train)
    >>> model.transform(df_test).show()
    """

    @keyword_only
    def __init__(  # pylint:disable=too-many-arguments
        self,
        *,
        features_col: Union[str, List[str]] = "features",
        label_col: str = "label",
        prediction_col: str = "prediction",
        pred_contrib_col: Optional[str] = None,
        validation_indicator_col: Optional[str] = None,
        weight_col: Optional[str] = None,
        base_margin_col: Optional[str] = None,
        qid_col: Optional[str] = None,
        num_workers: int = 1,
        use_gpu: Optional[bool] = None,
        device: Optional[str] = None,
        force_repartition: bool = False,
        repartition_random_shuffle: bool = False,
        enable_sparse_data_optim: bool = False,
        launch_tracker_on_driver: bool = True,
        coll_cfg: Optional[Config] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__()
        input_kwargs = self._input_kwargs
        if use_gpu:
            _deprecated_use_gpu()
        self.setParams(**input_kwargs)

    @classmethod
    def _xgb_cls(cls) -> Type[XGBRanker]:
        return XGBRanker

    @classmethod
    def _pyspark_model_cls(cls) -> Type["SparkXGBRankerModel"]:
        return SparkXGBRankerModel

    def _validate_params(self) -> None:
        super()._validate_params()
        if not self.isDefined(self.qid_col):
            raise ValueError(
                "Spark Xgboost ranker estimator requires setting `qid_col` param."
            )
