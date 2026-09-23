class EarlyStopping(TrainingCallback):
    """Callback function for early stopping

    .. versionadded:: 1.3.0

    Parameters
    ----------
    rounds :
        Early stopping rounds.
    metric_name :
        Name of metric that is used for early stopping.
    data_name :
        Name of dataset that is used for early stopping.
    maximize :
        Whether to maximize evaluation metric.  None means auto (discouraged).
    save_best :
        Whether training should return the best model or the last model. If set to
        `True`, it will only keep the boosting rounds up to the detected best iteration,
        discarding the ones that come after. This is only supported with tree methods
        (not `gblinear`). Also, the `cv` function doesn't return a model, the parameter
        is not applicable.
    min_delta :

        .. versionadded:: 1.5.0

        Minimum absolute change in score to be qualified as an improvement.

    Examples
    --------

    .. code-block:: python

        es = xgboost.callback.EarlyStopping(
            rounds=2,
            min_delta=1e-3,
            save_best=True,
            maximize=False,
            data_name="validation_0",
            metric_name="mlogloss",
        )
        clf = xgboost.XGBClassifier(tree_method="hist", device="cuda", callbacks=[es])

        X, y = load_digits(return_X_y=True)
        clf.fit(X, y, eval_set=[(X, y)])
    """

    # pylint: disable=too-many-arguments
    @_deprecate_positional_args
    def __init__(
        self,
        *,
        rounds: int,
        metric_name: Optional[str] = None,
        data_name: Optional[str] = None,
        maximize: Optional[bool] = None,
        save_best: Optional[bool] = False,
        min_delta: float = 0.0,
    ) -> None:
        self.data = data_name
        self.metric_name = metric_name
        self.rounds = rounds
        self.save_best = save_best
        self.maximize = maximize
        self.stopping_history: TrainingCallback.EvalsLog = {}
        self._min_delta = min_delta
        if self._min_delta < 0:
            raise ValueError("min_delta must be greater or equal to 0.")

        self.current_rounds: int = 0
        self.best_scores: dict = {}
        self.starting_round: int = 0
        super().__init__()

    def before_training(self, model: _Model) -> _Model:
        self.starting_round = model.num_boosted_rounds()
        if not isinstance(model, Booster) and self.save_best:
            raise ValueError(
                "`save_best` is not applicable to the `cv` function as it doesn't return"
                " a model."
            )
        return model

    def _update_rounds(
        self, *, score: _Score, name: str, metric: str, model: _Model, epoch: int
    ) -> bool:
        def get_s(value: _Score) -> float:
            """get score if it's cross validation history."""
            return value[0] if isinstance(value, tuple) else value

        def maximize(new: _Score, best: _Score) -> bool:
            """New score should be greater than the old one."""
            return numpy.greater(get_s(new) - self._min_delta, get_s(best))

        def minimize(new: _Score, best: _Score) -> bool:
            """New score should be lesser than the old one."""
            return numpy.greater(get_s(best) - self._min_delta, get_s(new))

        if self.maximize is None:
            # Just to be compatibility with old behavior before 1.3.  We should let
            # user to decide.
            maximize_metrics = (
                "auc",
                "aucpr",
                "pre",
                "pre@",
                "map",
                "ndcg",
                "auc@",
                "aucpr@",
                "map@",
                "ndcg@",
            )
            if metric != "mape" and any(metric.startswith(x) for x in maximize_metrics):
                self.maximize = True
            else:
                self.maximize = False

        if self.maximize:
            improve_op = maximize
        else:
            improve_op = minimize

        if not self.stopping_history:  # First round
            self.current_rounds = 0
            self.stopping_history[name] = {}
            self.stopping_history[name][metric] = cast(_ScoreList, [score])
            self.best_scores[name] = {}
            self.best_scores[name][metric] = [score]
            model.set_attr(best_score=str(get_s(score)), best_iteration=str(epoch))
        elif not improve_op(score, self.best_scores[name][metric][-1]):
            # Not improved
            self.stopping_history[name][metric].append(score)  # type: ignore
            self.current_rounds += 1
        else:  # Improved
            self.stopping_history[name][metric].append(score)  # type: ignore
            self.best_scores[name][metric].append(score)
            record = self.stopping_history[name][metric][-1]
            model.set_attr(best_score=str(get_s(record)), best_iteration=str(epoch))
            self.current_rounds = 0  # reset

        if self.current_rounds >= self.rounds:
            # Should stop
            return True
        return False

    def after_iteration(
        self, model: _Model, epoch: int, evals_log: TrainingCallback.EvalsLog
    ) -> bool:
        epoch += self.starting_round  # training continuation
        msg = "Must have at least 1 validation dataset for early stopping."
        if len(evals_log.keys()) < 1:
            raise ValueError(msg)

        # Get data name
        if self.data:
            data_name = self.data
        else:
            # Use the last one as default.
            data_name = list(evals_log.keys())[-1]
        if data_name not in evals_log:
            raise ValueError(f"No dataset named: {data_name}")

        if not isinstance(data_name, str):
            raise TypeError(
                f"The name of the dataset should be a string. Got: {type(data_name)}"
            )
        data_log = evals_log[data_name]

        # Get metric name
        if self.metric_name:
            metric_name = self.metric_name
        else:
            # Use last metric by default.
            metric_name = list(data_log.keys())[-1]
        if metric_name not in data_log:
            raise ValueError(f"No metric named: {metric_name}")

        # The latest score
        score = data_log[metric_name][-1]
        return self._update_rounds(
            score=score, name=data_name, metric=metric_name, model=model, epoch=epoch
        )

    def after_training(self, model: _Model) -> _Model:
        if not self.save_best:
            return model

        try:
            best_iteration = model.best_iteration
            best_score = model.best_score
            assert best_iteration is not None and best_score is not None
            model = model[: best_iteration + 1]
            model.best_iteration = best_iteration
            model.best_score = best_score
        except XGBoostError as e:
            raise XGBoostError(
                "`save_best` is not applicable to the current booster"
            ) from e

        return model
