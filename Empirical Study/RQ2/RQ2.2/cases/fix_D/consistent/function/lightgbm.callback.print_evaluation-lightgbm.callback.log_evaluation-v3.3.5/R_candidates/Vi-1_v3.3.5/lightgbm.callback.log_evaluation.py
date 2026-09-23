def log_evaluation(period: int = 1, show_stdv: bool = True) -> Callable:
    """Create a callback that logs the evaluation results.

    By default, standard output resource is used.
    Use ``register_logger()`` function to register a custom logger.

    Note
    ----
    Requires at least one validation data.

    Parameters
    ----------
    period : int, optional (default=1)
        The period to log the evaluation results.
        The last boosting stage or the boosting stage found by using ``early_stopping`` callback is also logged.
    show_stdv : bool, optional (default=True)
        Whether to log stdv (if provided).

    Returns
    -------
    callback : callable
        The callback that logs the evaluation results every ``period`` boosting iteration(s).
    """
    def _callback(env: CallbackEnv) -> None:
        if period > 0 and env.evaluation_result_list and (env.iteration + 1) % period == 0:
            result = '\t'.join([_format_eval_result(x, show_stdv) for x in env.evaluation_result_list])
            _log_info(f'[{env.iteration + 1}]\t{result}')
    _callback.order = 10  # type: ignore
    return _callback
