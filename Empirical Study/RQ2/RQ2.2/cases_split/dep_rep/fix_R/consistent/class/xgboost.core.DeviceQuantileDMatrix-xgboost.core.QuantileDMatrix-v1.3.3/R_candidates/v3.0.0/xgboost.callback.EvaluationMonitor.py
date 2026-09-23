class EvaluationMonitor(TrainingCallback):
    """Print the evaluation result at each iteration.

    .. versionadded:: 1.3.0

    Parameters
    ----------

    rank :
        Which worker should be used for printing the result.
    period :
        How many epoches between printing.
    show_stdv :
        Used in cv to show standard deviation.  Users should not specify it.
    logger :
        A callable used for logging evaluation result.

    """

    def __init__(
        self,
        rank: int = 0,
        period: int = 1,
        show_stdv: bool = False,
        logger: Callable[[str], None] = collective.communicator_print,
    ):
        self.printer_rank = rank
        self.show_stdv = show_stdv
        self.period = period
        self._logger = logger
        assert period > 0
        # last error message, useful when early stopping and period are used together.
        self._latest: Optional[str] = None
        super().__init__()

    def _fmt_metric(
        self, data: str, metric: str, score: float, std: Optional[float]
    ) -> str:
        if std is not None and self.show_stdv:
            msg = f"\t{data + '-' + metric}:{score:.5f}+{std:.5f}"
        else:
            msg = f"\t{data + '-' + metric}:{score:.5f}"
        return msg

    def after_iteration(
        self, model: _Model, epoch: int, evals_log: TrainingCallback.EvalsLog
    ) -> bool:
        if not evals_log:
            return False

        msg: str = f"[{epoch}]"
        if collective.get_rank() == self.printer_rank:
            for data, metric in evals_log.items():
                for metric_name, log in metric.items():
                    stdv: Optional[float] = None
                    if isinstance(log[-1], tuple):
                        score = log[-1][0]
                        stdv = log[-1][1]
                    else:
                        score = log[-1]
                    msg += self._fmt_metric(data, metric_name, score, stdv)
            msg += "\n"

            if (epoch % self.period) == 0 or self.period == 1:
                self._logger(msg)
                self._latest = None
            else:
                # There is skipped message
                self._latest = msg
        return False

    def after_training(self, model: _Model) -> _Model:
        if collective.get_rank() == self.printer_rank and self._latest is not None:
            self._logger(self._latest)
        return model
