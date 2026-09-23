class TrainingCallback(ABC):
    """Interface for training callback.

    .. versionadded:: 1.3.0

    """

    EvalsLog = Dict[str, Dict[str, _ScoreList]]  # pylint: disable=invalid-name

    def __init__(self) -> None:
        pass

    def before_training(self, model: _Model) -> _Model:
        """Run before training starts."""
        return model

    def after_training(self, model: _Model) -> _Model:
        """Run after training is finished."""
        return model

    def before_iteration(self, model: _Model, epoch: int, evals_log: EvalsLog) -> bool:
        """Run before each iteration.  Returns True when training should stop. See
        :py:meth:`after_iteration` for details.

        """
        return False

    def after_iteration(self, model: _Model, epoch: int, evals_log: EvalsLog) -> bool:
        """Run after each iteration.  Returns `True` when training should stop.

        Parameters
        ----------

        model :
            Eeither a :py:class:`~xgboost.Booster` object or a CVPack if the cv function
            in xgboost is being used.
        epoch :
            The current training iteration.
        evals_log :
            A dictionary containing the evaluation history:

            .. code-block:: python

                {"data_name": {"metric_name": [0.5, ...]}}

        """
        return False
