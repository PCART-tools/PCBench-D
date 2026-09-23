def executor_test_settings(func):
    if hu.is_sandcastle() or hu.is_travis():
        return hu.settings(
            max_examples=CI_MAX_EXAMPLES,
            deadline=CI_TIMEOUT * 1000  # deadline is in ms
        )(func)
    else:
        return func
