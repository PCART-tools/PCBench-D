@xgboost_model_doc(
    "Implementation of the scikit-learn API for XGBoost regression.",
    ["estimators", "model", "objective"],
)
class XGBRegressor(XGBRegressorBase, XGBModel):
    # pylint: disable=missing-docstring
    @_deprecate_positional_args
    def __init__(
        self, *, objective: SklObjective = "reg:squarederror", **kwargs: Any
    ) -> None:
        super().__init__(objective=objective, **kwargs)

    def _more_tags(self) -> Dict[str, bool]:
        tags = super()._more_tags()
        tags["multioutput"] = True
        tags["multioutput_only"] = False
        return tags

    def __sklearn_tags__(self) -> _sklearn_Tags:
        tags = super().__sklearn_tags__()
        tags_dict = self._more_tags()
        tags.target_tags.multi_output = tags_dict["multioutput"]
        tags.target_tags.single_output = not tags_dict["multioutput_only"]
        return tags
