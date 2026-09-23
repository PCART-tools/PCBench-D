@xgboost_model_doc(
    """Implementation of the Scikit-Learn API for XGBoost Random Forest Regressor.

    .. versionadded:: 1.4.0

""",
    ["model", "objective"],
    extra_parameters="""
    n_estimators : int
        Number of trees in random forest to fit.
""",
)
class DaskXGBRFRegressor(DaskXGBRegressor):
    @_deprecate_positional_args
    def __init__(
        self,
        *,
        learning_rate: Optional[float] = 1,
        subsample: Optional[float] = 0.8,
        colsample_bynode: Optional[float] = 0.8,
        reg_lambda: Optional[float] = 1e-5,
        coll_cfg: Optional[CollConfig] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            learning_rate=learning_rate,
            subsample=subsample,
            colsample_bynode=colsample_bynode,
            reg_lambda=reg_lambda,
            coll_cfg=coll_cfg,
            **kwargs,
        )

    def get_xgb_params(self) -> Dict[str, Any]:
        params = super().get_xgb_params()
        params["num_parallel_tree"] = self.n_estimators
        return params

    def get_num_boosting_rounds(self) -> int:
        return 1

    # pylint: disable=unused-argument
    def fit(
        self,
        X: _DataT,
        y: _DaskCollection,
        *,
        sample_weight: Optional[_DaskCollection] = None,
        base_margin: Optional[_DaskCollection] = None,
        eval_set: Optional[Sequence[Tuple[_DaskCollection, _DaskCollection]]] = None,
        verbose: Optional[Union[int, bool]] = True,
        xgb_model: Optional[Union[Booster, str, XGBModel]] = None,
        sample_weight_eval_set: Optional[Sequence[_DaskCollection]] = None,
        base_margin_eval_set: Optional[Sequence[_DaskCollection]] = None,
        feature_weights: Optional[_DaskCollection] = None,
    ) -> "DaskXGBRFRegressor":
        args = {k: v for k, v in locals().items() if k not in ("self", "__class__")}
        _check_rf_callback(self.early_stopping_rounds, self.callbacks)
        super().fit(**args)
        return self
