@xgboost_model_doc(
    "scikit-learn API for XGBoost random forest classification.",
    ["model", "objective"],
    extra_parameters="""
    n_estimators : Optional[int]
        Number of trees in random forest to fit.
""",
)
class XGBRFClassifier(XGBClassifier):
    # pylint: disable=missing-docstring
    @_deprecate_positional_args
    def __init__(
        self,
        *,
        learning_rate: float = 1.0,
        subsample: float = 0.8,
        colsample_bynode: float = 0.8,
        reg_lambda: float = 1e-5,
        **kwargs: Any,
    ):
        super().__init__(
            learning_rate=learning_rate,
            subsample=subsample,
            colsample_bynode=colsample_bynode,
            reg_lambda=reg_lambda,
            **kwargs,
        )
        _check_rf_callback(self.early_stopping_rounds, self.callbacks)

    def get_xgb_params(self) -> Dict[str, Any]:
        params = super().get_xgb_params()
        params["num_parallel_tree"] = super().get_num_boosting_rounds()
        return params

    def get_num_boosting_rounds(self) -> int:
        return 1

    # pylint: disable=unused-argument
    @_deprecate_positional_args
    def fit(
        self,
        X: ArrayLike,
        y: ArrayLike,
        *,
        sample_weight: Optional[ArrayLike] = None,
        base_margin: Optional[ArrayLike] = None,
        eval_set: Optional[Sequence[Tuple[ArrayLike, ArrayLike]]] = None,
        verbose: Optional[Union[bool, int]] = True,
        xgb_model: Optional[Union[Booster, str, XGBModel]] = None,
        sample_weight_eval_set: Optional[Sequence[ArrayLike]] = None,
        base_margin_eval_set: Optional[Sequence[ArrayLike]] = None,
        feature_weights: Optional[ArrayLike] = None,
    ) -> "XGBRFClassifier":
        args = {k: v for k, v in locals().items() if k not in ("self", "__class__")}
        _check_rf_callback(self.early_stopping_rounds, self.callbacks)
        super().fit(**args)
        return self
