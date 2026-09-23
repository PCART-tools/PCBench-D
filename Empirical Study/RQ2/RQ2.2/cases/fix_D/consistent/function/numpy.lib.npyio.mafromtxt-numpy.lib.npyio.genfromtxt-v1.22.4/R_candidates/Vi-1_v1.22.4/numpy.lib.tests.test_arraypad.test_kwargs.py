@pytest.mark.parametrize("mode", _all_modes.keys())
def test_kwargs(mode):
    """Test behavior of pad's kwargs for the given mode."""
    allowed = _all_modes[mode]
    not_allowed = {}
    for kwargs in _all_modes.values():
        if kwargs != allowed:
            not_allowed.update(kwargs)
    # Test if allowed keyword arguments pass
    np.pad([1, 2, 3], 1, mode, **allowed)
    # Test if prohibited keyword arguments of other modes raise an error
    for key, value in not_allowed.items():
        match = "unsupported keyword arguments for mode '{}'".format(mode)
        with pytest.raises(ValueError, match=match):
            np.pad([1, 2, 3], 1, mode, **{key: value})
