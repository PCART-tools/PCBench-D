def print_evaluation(period: int = 1, show_stdv: bool = True) -> Callable:
    """Create a callback that logs the evaluation results.

    Deprecated, use ``log_evaluation()`` instead.
    """
    _log_warning("'print_evaluation()' callback is deprecated and will be removed in a future release of LightGBM. "
                 "Use 'log_evaluation()' callback instead.")
    return log_evaluation(period=period, show_stdv=show_stdv)
