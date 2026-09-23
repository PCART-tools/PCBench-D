@xgboost_model_doc(
    """Implementation of the Scikit-Learn API for XGBoost Ranking.

See :doc:`Learning to Rank </tutorials/learning_to_rank>` for an introducion.

    """,
    ["estimators", "model"],
    end_note="""
        .. note::

            A custom objective function is currently not supported by XGBRanker.

        .. note::

            Query group information is only required for ranking training but not
            prediction. Multiple groups can be predicted on a single call to
            :py:meth:`predict`.

        When fitting the model with the `group` parameter, your data need to be sorted
        by the query group first. `group` is an array that contains the size of each
        query group.

        Similarly, when fitting the model with the `qid` parameter, the data should be
        sorted according to query index and `qid` is an array that contains the query
        index for each training sample.

        For example, if your original data look like:

        +-------+-----------+---------------+
        |   qid |   label   |   features    |
        +-------+-----------+---------------+
        |   1   |   0       |   x_1         |
        +-------+-----------+---------------+
        |   1   |   1       |   x_2         |
        +-------+-----------+---------------+
        |   1   |   0       |   x_3         |
        +-------+-----------+---------------+
        |   2   |   0       |   x_4         |
        +-------+-----------+---------------+
        |   2   |   1       |   x_5         |
        +-------+-----------+---------------+
        |   2   |   1       |   x_6         |
        +-------+-----------+---------------+
        |   2   |   1       |   x_7         |
        +-------+-----------+---------------+

        then :py:meth:`fit` method can be called with either `group` array as ``[3, 4]``
        or with `qid` as ``[1, 1, 1, 2, 2, 2, 2]``, that is the qid column.  Also, the
        `qid` can be a special column of input `X` instead of a separated parameter, see
        :py:meth:`fit` for more info.""",
)
class XGBRanker(XGBRankerMixIn, XGBModel):
    # pylint: disable=missing-docstring,too-many-arguments,invalid-name
    @_deprecate_positional_args
    def __init__(self, *, objective: str = "rank:ndcg", **kwargs: Any):
        super().__init__(objective=objective, **kwargs)
        if callable(self.objective):
            raise ValueError("custom objective function not supported by XGBRanker")
        if "rank:" not in objective:
            raise ValueError("please use XGBRanker for ranking task")

    def _create_ltr_dmatrix(
        self, ref: Optional[DMatrix], data: ArrayLike, qid: ArrayLike, **kwargs: Any
    ) -> DMatrix:
        data, qid = _get_qid(data, qid)

        if kwargs.get("group", None) is None and qid is None:
            raise ValueError("Either `group` or `qid` is required for ranking task")

        return super()._create_dmatrix(ref=ref, data=data, qid=qid, **kwargs)

    @_deprecate_positional_args
    def fit(
        self,
        X: ArrayLike,
        y: ArrayLike,
        *,
        group: Optional[ArrayLike] = None,
        qid: Optional[ArrayLike] = None,
        sample_weight: Optional[ArrayLike] = None,
        base_margin: Optional[ArrayLike] = None,
        eval_set: Optional[Sequence[Tuple[ArrayLike, ArrayLike]]] = None,
        eval_group: Optional[Sequence[ArrayLike]] = None,
        eval_qid: Optional[Sequence[ArrayLike]] = None,
        verbose: Optional[Union[bool, int]] = False,
        xgb_model: Optional[Union[Booster, str, XGBModel]] = None,
        sample_weight_eval_set: Optional[Sequence[ArrayLike]] = None,
        base_margin_eval_set: Optional[Sequence[ArrayLike]] = None,
        feature_weights: Optional[ArrayLike] = None,
    ) -> "XGBRanker":
        # pylint: disable = attribute-defined-outside-init,arguments-differ
        """Fit gradient boosting ranker

        Note that calling ``fit()`` multiple times will cause the model object to be
        re-fit from scratch. To resume training from a previous checkpoint, explicitly
        pass ``xgb_model`` argument.

        Parameters
        ----------
        X :
            Feature matrix. See :ref:`py-data` for a list of supported types.

            When this is a :py:class:`pandas.DataFrame` or a :py:class:`cudf.DataFrame`,
            it may contain a special column called ``qid`` for specifying the query
            index. Using a special column is the same as using the `qid` parameter,
            except for being compatible with sklearn utility functions like
            :py:func:`sklearn.model_selection.cross_validation`. The same convention
            applies to the :py:meth:`XGBRanker.score` and :py:meth:`XGBRanker.predict`.

            +-----+----------------+----------------+
            | qid | feat_0         | feat_1         |
            +-----+----------------+----------------+
            | 0   | :math:`x_{00}` | :math:`x_{01}` |
            +-----+----------------+----------------+
            | 1   | :math:`x_{10}` | :math:`x_{11}` |
            +-----+----------------+----------------+
            | 1   | :math:`x_{20}` | :math:`x_{21}` |
            +-----+----------------+----------------+

            When the ``tree_method`` is set to ``hist``, internally, the
            :py:class:`QuantileDMatrix` will be used instead of the :py:class:`DMatrix`
            for conserving memory. However, this has performance implications when the
            device of input data is not matched with algorithm. For instance, if the
            input is a numpy array on CPU but ``cuda`` is used for training, then the
            data is first processed on CPU then transferred to GPU.
        y :
            Labels
        group :
            Size of each query group of training data. Should have as many elements as
            the query groups in the training data.  If this is set to None, then user
            must provide qid.
        qid :
            Query ID for each training sample.  Should have the size of n_samples.  If
            this is set to None, then user must provide group or a special column in X.
        sample_weight :
            Query group weights

            .. note:: Weights are per-group for ranking tasks

                In ranking task, one weight is assigned to each query group/id (not each
                data point). This is because we only care about the relative ordering of
                data points within each group, so it doesn't make sense to assign
                weights to individual data points.

        base_margin :
            Global bias for each instance. See :doc:`/tutorials/intercept` for details.
        eval_set :
            A list of (X, y) tuple pairs to use as validation sets, for which
            metrics will be computed.
            Validation metrics will help us track the performance of the model.
        eval_group :
            A list in which ``eval_group[i]`` is the list containing the sizes of all
            query groups in the ``i``-th pair in **eval_set**.
        eval_qid :
            A list in which ``eval_qid[i]`` is the array containing query ID of ``i``-th
            pair in **eval_set**. The special column convention in `X` applies to
            validation datasets as well.

        verbose :
            If `verbose` is True and an evaluation set is used, the evaluation metric
            measured on the validation set is printed to stdout at each boosting stage.
            If `verbose` is an integer, the evaluation metric is printed at each
            `verbose` boosting stage. The last boosting stage / the boosting stage found
            by using `early_stopping_rounds` is also printed.
        xgb_model :
            file name of stored XGBoost model or 'Booster' instance XGBoost model to be
            loaded before training (allows training continuation).
        sample_weight_eval_set :
            A list of the form [L_1, L_2, ..., L_n], where each L_i is a list of
            group weights on the i-th validation set.

            .. note:: Weights are per-group for ranking tasks

                In ranking task, one weight is assigned to each query group (not each
                data point). This is because we only care about the relative ordering of
                data points within each group, so it doesn't make sense to assign
                weights to individual data points.
        base_margin_eval_set :
            A list of the form [M_1, M_2, ..., M_n], where each M_i is an array like
            object storing base margin for the i-th validation set.
        feature_weights :
            Weight for each feature, defines the probability of each feature being
            selected when colsample is being used.  All values must be greater than 0,
            otherwise a `ValueError` is thrown.

        """
        with config_context(verbosity=self.verbosity):
            train_dmatrix, evals = _wrap_evaluation_matrices(
                missing=self.missing,
                X=X,
                y=y,
                group=group,
                qid=qid,
                sample_weight=sample_weight,
                base_margin=base_margin,
                feature_weights=feature_weights,
                eval_set=eval_set,
                sample_weight_eval_set=sample_weight_eval_set,
                base_margin_eval_set=base_margin_eval_set,
                eval_group=eval_group,
                eval_qid=eval_qid,
                create_dmatrix=self._create_ltr_dmatrix,
                enable_categorical=self.enable_categorical,
                feature_types=self.feature_types,
            )

            evals_result: TrainingCallback.EvalsLog = {}
            params = self.get_xgb_params()

            model, metric, params, feature_weights = self._configure_fit(
                xgb_model, params, feature_weights
            )
            self._Booster = train(
                params,
                train_dmatrix,
                num_boost_round=self.get_num_boosting_rounds(),
                early_stopping_rounds=self.early_stopping_rounds,
                evals=evals,
                evals_result=evals_result,
                custom_metric=metric,
                verbose_eval=verbose,
                xgb_model=model,
                callbacks=self.callbacks,
            )

            self.objective = params["objective"]

            self._set_evaluation_result(evals_result)
            return self

    @_deprecate_positional_args
    def predict(
        self,
        X: ArrayLike,
        *,
        output_margin: bool = False,
        validate_features: bool = True,
        base_margin: Optional[ArrayLike] = None,
        iteration_range: Optional[IterationRange] = None,
    ) -> ArrayLike:
        X, _ = _get_qid(X, None)
        return super().predict(
            X,
            output_margin=output_margin,
            validate_features=validate_features,
            base_margin=base_margin,
            iteration_range=iteration_range,
        )

    def apply(
        self,
        X: ArrayLike,
        iteration_range: Optional[IterationRange] = None,
    ) -> ArrayLike:
        X, _ = _get_qid(X, None)
        return super().apply(X, iteration_range)

    def score(self, X: ArrayLike, y: ArrayLike) -> float:
        """Evaluate score for data using the last evaluation metric. If the model is
        trained with early stopping, then :py:attr:`best_iteration` is used
        automatically.

        Parameters
        ----------
        X : Union[pd.DataFrame, cudf.DataFrame]
          Feature matrix. A DataFrame with a special `qid` column.

        y :
          Labels

        Returns
        -------
        score :
          The result of the first evaluation metric for the ranker.

        """
        X, qid = _get_qid(X, None)
        # fixme(jiamingy): base margin and group weight is not yet supported. We might
        # need to make extra special fields in the dataframe.
        Xyq = DMatrix(
            X,
            y,
            qid=qid,
            missing=self.missing,
            enable_categorical=self.enable_categorical,
            nthread=self.n_jobs,
            feature_types=self.feature_types,
        )
        if callable(self.eval_metric):
            metric = ltr_metric_decorator(self.eval_metric, self.n_jobs)
            result_str = self.get_booster().eval_set([(Xyq, "eval")], feval=metric)
        else:
            result_str = self.get_booster().eval(Xyq)

        metric_score = _parse_eval_str(result_str)
        return metric_score[-1][1]
