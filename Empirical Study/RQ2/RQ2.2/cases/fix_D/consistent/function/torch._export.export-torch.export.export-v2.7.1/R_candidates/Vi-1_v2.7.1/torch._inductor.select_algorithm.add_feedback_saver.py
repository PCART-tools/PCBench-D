def add_feedback_saver(
    fn: Callable[[dict[ChoiceCaller, float], str, list[Any], list[ChoiceCaller]], None],
):
    global _ALGORITHM_SELECTOR_CACHE
    if _ALGORITHM_SELECTOR_CACHE is None:
        _ALGORITHM_SELECTOR_CACHE = AlgorithmSelectorCache()
    _ALGORITHM_SELECTOR_CACHE.add_feedback_saver(fn)
