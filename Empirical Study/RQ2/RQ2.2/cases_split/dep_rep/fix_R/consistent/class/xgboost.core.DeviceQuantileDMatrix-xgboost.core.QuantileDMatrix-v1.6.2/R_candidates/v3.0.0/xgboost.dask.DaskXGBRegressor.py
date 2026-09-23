@xgboost_model_doc(
    """Implementation of the Scikit-Learn API for XGBoost.""", ["estimators", "model"]
)
class DaskXGBRegressor(XGBRegressorBase, DaskScikitLearnBase):
    """dummy doc string to workaround pylint, replaced by the decorator."""

    async def _fit_async(
        self,
        X: _DataT,
        y: _DaskCollection,
        *,
        sample_weight: Optional[_DaskCollection],
        base_margin: Optional[_DaskCollection],
        eval_set: Optional[Sequence[Tuple[_DaskCollection, _DaskCollection]]],
        sample_weight_eval_set: Optional[Sequence[_DaskCollection]],
        base_margin_eval_set: Optional[Sequence[_DaskCollection]],
        verbose: Union[int, bool],
        xgb_model: Optional[Union[Booster, XGBModel]],
        feature_weights: Optional[_DaskCollection],
    ) -> _DaskCollection:
        params = self.get_xgb_params()
        model, metric, params, feature_weights = self._configure_fit(
            xgb_model, params, feature_weights
        )

        dtrain, evals = await _async_wrap_evaluation_matrices(
            client=self.client,
            device=self.device,
            tree_method=self.tree_method,
            max_bin=self.max_bin,
            X=X,
            y=y,
            group=None,
            qid=None,
            sample_weight=sample_weight,
            base_margin=base_margin,
            feature_weights=feature_weights,
            eval_set=eval_set,
            sample_weight_eval_set=sample_weight_eval_set,
            base_margin_eval_set=base_margin_eval_set,
            eval_group=None,
            eval_qid=None,
            missing=self.missing,
            enable_categorical=self.enable_categorical,
            feature_types=self.feature_types,
        )

        if callable(self.objective):
            obj: Optional[Callable] = _objective_decorator(self.objective)
        else:
            obj = None
        results = await self.client.sync(
            _train_async,
            asynchronous=True,
            client=self.client,
            global_config=config.get_config(),
            dconfig=_get_dask_config(),
            params=params,
            dtrain=dtrain,
            num_boost_round=self.get_num_boosting_rounds(),
            evals=evals,
            obj=obj,
            custom_metric=metric,
            verbose_eval=verbose,
            early_stopping_rounds=self.early_stopping_rounds,
            callbacks=self.callbacks,
            coll_cfg=self.coll_cfg,
            xgb_model=model,
        )
        self._Booster = results["booster"]
        self._set_evaluation_result(results["history"])
        return self

    # pylint: disable=missing-docstring, disable=unused-argument
    @_deprecate_positional_args
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
    ) -> "DaskXGBRegressor":
        args = {k: v for k, v in locals().items() if k not in ("self", "__class__")}
        return self._client_sync(self._fit_async, **args)
