def _check_tuning_assertions() -> None:
    r"""Helper function for multi-GPU tuning case. Need to check that TunableOp feature
    is enabled and that tuning is enabled.
    """

    if is_enabled() is False:
        warnings.warn("TunableOp was disabled. Trying to enable now.")
        enable(True)
    assert is_enabled() is True
    assert tuning_is_enabled() is True
    assert record_untuned_is_enabled() is False
