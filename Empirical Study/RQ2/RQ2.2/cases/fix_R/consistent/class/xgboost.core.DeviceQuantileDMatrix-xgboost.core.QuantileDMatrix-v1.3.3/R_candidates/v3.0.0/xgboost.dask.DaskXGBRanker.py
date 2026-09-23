@xgboost_model_doc(
    """Implementation of the Scikit-Learn API for XGBoost Ranking.

    .. versionadded:: 1.4.0

""",
    ["estimators", "model"],
    extra_parameters="""
    allow_group_split :

        .. versionadded:: 3.0.0

        Whether a query group can be split among multiple workers. When set to `False`,
        inputs must be Dask dataframes or series. If you have many small query groups,
        this can significantly increase the fragmentation of the data, and the internal
        DMatrix construction can take longer.

""",
    end_note="""
        .. note::

            For the dask implementation, group is not supported, use qid instead.
""",
)
class DaskXGBRanker(XGBRankerMixIn, DaskScikitLearnBase):
    @_deprecate_positional_args
    def __init__(
        self,
        *,
        objective: str = "rank:pairwise",
        allow_group_split: bool = False,
        coll_cfg: Optional[CollConfig] = None,
        **kwargs: Any,
    ) -> None:
        if callable(objective):
            raise ValueError("Custom objective function not supported by XGBRanker.")
        self.allow_group_split = allow_group_split
        super().__init__(objective=objective, coll_cfg=coll_cfg, **kwargs)

    def _wrapper_params(self) -> Set[str]:
        params = super()._wrapper_params()
        params.add("allow_group_split")
        return params

    async def _fit_async(
        self,
        X: _DataT,
        y: _DaskCollection,
        *,
        qid: Optional[_DaskCollection],
        sample_weight: Optional[_DaskCollection],
        base_margin: Optional[_DaskCollection],
        eval_set: Optional[Sequence[Tuple[_DaskCollection, _DaskCollection]]],
        sample_weight_eval_set: Optional[Sequence[_DaskCollection]],
        base_margin_eval_set: Optional[Sequence[_DaskCollection]],
        eval_qid: Optional[Sequence[_DaskCollection]],
        verbose: Union[int, bool],
        xgb_model: Optional[Union[XGBModel, Booster]],
        feature_weights: Optional[_DaskCollection],
    ) -> "DaskXGBRanker":
        params = self.get_xgb_params()
        model, metric, params, feature_weights = self._configure_fit(
            xgb_model, params, feature_weights
        )
        dtrain, evals = await _async_wrap_evaluation_matrices(
            self.client,
            device=self.device,
            tree_method=self.tree_method,
            max_bin=self.max_bin,
            X=X,
            y=y,
            group=None,
            qid=qid,
            sample_weight=sample_weight,
            base_margin=base_margin,
            feature_weights=feature_weights,
            eval_set=eval_set,
            sample_weight_eval_set=sample_weight_eval_set,
            base_margin_eval_set=base_margin_eval_set,
            eval_group=None,
            eval_qid=eval_qid,
            missing=self.missing,
            enable_categorical=self.enable_categorical,
            feature_types=self.feature_types,
        )
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
            obj=None,
            custom_metric=metric,
            verbose_eval=verbose,
            early_stopping_rounds=self.early_stopping_rounds,
            callbacks=self.callbacks,
            xgb_model=model,
            coll_cfg=self.coll_cfg,
        )
        self._Booster = results["booster"]
        self.evals_result_ = results["history"]
        return self

    # pylint: disable=unused-argument, arguments-differ
    @_deprecate_positional_args
    def fit(
        self,
        X: _DataT,
        y: _DaskCollection,
        *,
        group: Optional[_DaskCollection] = None,
        qid: Optional[_DaskCollection] = None,
        sample_weight: Optional[_DaskCollection] = None,
        base_margin: Optional[_DaskCollection] = None,
        eval_set: Optional[Sequence[Tuple[_DaskCollection, _DaskCollection]]] = None,
        eval_group: Optional[Sequence[_DaskCollection]] = None,
        eval_qid: Optional[Sequence[_DaskCollection]] = None,
        verbose: Optional[Union[int, bool]] = False,
        xgb_model: Optional[Union[XGBModel, str, Booster]] = None,
        sample_weight_eval_set: Optional[Sequence[_DaskCollection]] = None,
        base_margin_eval_set: Optional[Sequence[_DaskCollection]] = None,
        feature_weights: Optional[_DaskCollection] = None,
    ) -> "DaskXGBRanker":
        msg = "Use the `qid` instead of the `group` with the dask interface."
        if not (group is None and eval_group is None):
            raise ValueError(msg)
        if qid is None:
            raise ValueError("`qid` is required for ranking.")

        def check_df(X: _DaskCollection) -> TypeGuard[dd.DataFrame]:
            if not isinstance(X, dd.DataFrame):
                raise TypeError(
                    "When `allow_group_split` is set to False, X is required to be"
                    " a dataframe."
                )
            return True

        def check_ser(
            qid: Optional[_DaskCollection], name: str
        ) -> TypeGuard[Optional[dd.Series]]:
            if not isinstance(qid, dd.Series) and qid is not None:
                raise TypeError(
                    f"When `allow_group_split` is set to False, {name} is required to be"
                    " a series."
                )
            return True

        if not self.allow_group_split:
            assert (
                check_df(X)
                and check_ser(qid, "qid")
                and check_ser(y, "y")
                and check_ser(sample_weight, "sample_weight")
                and check_ser(base_margin, "base_margin")
            )
            assert qid is not None and y is not None
            X_id = id(X)
            X, qid, y, sample_weight, base_margin = no_group_split(
                self.device,
                X,
                qid,
                y=y,
                sample_weight=sample_weight,
                base_margin=base_margin,
            )

            if eval_set is not None:
                new_eval_set = []
                new_eval_qid = []
                new_sample_weight_eval_set = []
                new_base_margin_eval_set = []
                assert eval_qid
                for i, (Xe, ye) in enumerate(eval_set):
                    we = sample_weight_eval_set[i] if sample_weight_eval_set else None
                    be = base_margin_eval_set[i] if base_margin_eval_set else None
                    assert check_df(Xe)
                    assert eval_qid
                    qe = eval_qid[i]
                    assert (
                        eval_qid
                        and check_ser(qe, "qid")
                        and check_ser(ye, "y")
                        and check_ser(we, "sample_weight")
                        and check_ser(be, "base_margin")
                    )
                    assert qe is not None and ye is not None
                    if id(Xe) != X_id:
                        Xe, qe, ye, we, be = no_group_split(
                            self.device, Xe, qe, ye, we, be
                        )
                    else:
                        Xe, qe, ye, we, be = X, qid, y, sample_weight, base_margin

                    new_eval_set.append((Xe, ye))
                    new_eval_qid.append(qe)

                    if we is not None:
                        new_sample_weight_eval_set.append(we)
                    if be is not None:
                        new_base_margin_eval_set.append(be)

                eval_set = new_eval_set
                eval_qid = new_eval_qid
                sample_weight_eval_set = (
                    new_sample_weight_eval_set if new_sample_weight_eval_set else None
                )
                base_margin_eval_set = (
                    new_base_margin_eval_set if new_base_margin_eval_set else None
                )

        return self._client_sync(
            self._fit_async,
            X=X,
            y=y,
            qid=qid,
            sample_weight=sample_weight,
            base_margin=base_margin,
            eval_set=eval_set,
            eval_qid=eval_qid,
            verbose=verbose,
            xgb_model=xgb_model,
            sample_weight_eval_set=sample_weight_eval_set,
            base_margin_eval_set=base_margin_eval_set,
            feature_weights=feature_weights,
        )

    # FIXME(trivialfis): arguments differ due to additional parameters like group and
    # qid.
    fit.__doc__ = XGBRanker.fit.__doc__
