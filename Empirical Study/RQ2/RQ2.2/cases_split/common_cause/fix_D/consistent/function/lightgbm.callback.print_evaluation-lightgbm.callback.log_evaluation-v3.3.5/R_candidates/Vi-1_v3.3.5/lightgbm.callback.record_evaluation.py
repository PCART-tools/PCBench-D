def record_evaluation(eval_result: Dict[str, Dict[str, List[Any]]]) -> Callable:
    """Create a callback that records the evaluation history into ``eval_result``.

    Parameters
    ----------
    eval_result : dict
        Dictionary used to store all evaluation results of all validation sets.
        This should be initialized outside of your call to ``record_evaluation()`` and should be empty.
        Any initial contents of the dictionary will be deleted.

        .. rubric:: Example

        With two validation sets named 'eval' and 'train', and one evaluation metric named 'logloss'
        this dictionary after finishing a model training process will have the following structure:

        .. code-block::

            {
             'train':
                 {
                  'logloss': [0.48253, 0.35953, ...]
                 },
             'eval':
                 {
                  'logloss': [0.480385, 0.357756, ...]
                 }
            }

    Returns
    -------
    callback : callable
        The callback that records the evaluation history into the passed dictionary.
    """
    if not isinstance(eval_result, dict):
        raise TypeError('eval_result should be a dictionary')
    eval_result.clear()

    def _init(env: CallbackEnv) -> None:
        for data_name, eval_name, _, _ in env.evaluation_result_list:
            eval_result.setdefault(data_name, collections.OrderedDict())
            eval_result[data_name].setdefault(eval_name, [])

    def _callback(env: CallbackEnv) -> None:
        if not eval_result:
            _init(env)
        for data_name, eval_name, result, _ in env.evaluation_result_list:
            eval_result[data_name][eval_name].append(result)
    _callback.order = 20  # type: ignore
    return _callback
