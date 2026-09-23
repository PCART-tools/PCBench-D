def assert_deadline_disabled():
    if hypothesis_version < (3, 27, 0):
        import warnings
        warning_message = (
            "Your version of hypothesis is outdated. "
            "To avoid `DeadlineExceeded` errors, please update. "
            "Current hypothesis version: {}".format(hypothesis.__version__)
        )
        warnings.warn(warning_message)
    else:
        assert settings().deadline is None
