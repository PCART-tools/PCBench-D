class LearningRateScheduler(TrainingCallback):
    """Callback function for scheduling learning rate.

    .. versionadded:: 1.3.0

    Parameters
    ----------

    learning_rates :
        If it's a callable object, then it should accept an integer parameter
        `epoch` and returns the corresponding learning rate.  Otherwise it
        should be a sequence like list or tuple with the same size of boosting
        rounds.

    """

    def __init__(
        self, learning_rates: Union[Callable[[int], float], Sequence[float]]
    ) -> None:
        if not callable(learning_rates) and not isinstance(
            learning_rates, collections.abc.Sequence
        ):
            raise TypeError(
                "Invalid learning rates, expecting callable or sequence, got: "
                f"{type(learning_rates)}"
            )

        if callable(learning_rates):
            self.learning_rates = learning_rates
        else:
            self.learning_rates = lambda epoch: cast(Sequence, learning_rates)[epoch]
        super().__init__()

    def after_iteration(
        self, model: _Model, epoch: int, evals_log: TrainingCallback.EvalsLog
    ) -> bool:
        model.set_param("learning_rate", self.learning_rates(epoch))
        return False
