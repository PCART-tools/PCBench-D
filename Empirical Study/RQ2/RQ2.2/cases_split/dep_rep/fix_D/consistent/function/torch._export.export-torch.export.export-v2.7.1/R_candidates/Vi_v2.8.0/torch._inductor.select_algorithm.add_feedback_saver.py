def add_feedback_saver(
    fn: FeedbackFunction,
):
    global _ALGORITHM_SELECTOR_CACHE
    if _ALGORITHM_SELECTOR_CACHE is None:
        _ALGORITHM_SELECTOR_CACHE = AlgorithmSelectorCache()
    _ALGORITHM_SELECTOR_CACHE.add_feedback_saver(fn)
