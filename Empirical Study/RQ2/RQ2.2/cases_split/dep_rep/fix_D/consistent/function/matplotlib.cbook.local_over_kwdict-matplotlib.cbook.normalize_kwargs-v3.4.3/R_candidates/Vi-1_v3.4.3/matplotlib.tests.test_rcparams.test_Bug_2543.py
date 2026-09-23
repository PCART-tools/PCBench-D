def test_Bug_2543():
    # Test that it possible to add all values to itself / deepcopy
    # This was not possible because validate_bool_maybe_none did not
    # accept None as an argument.
    # https://github.com/matplotlib/matplotlib/issues/2543
    # We filter warnings at this stage since a number of them are raised
    # for deprecated rcparams as they should. We don't want these in the
    # printed in the test suite.
    with _api.suppress_matplotlib_deprecation_warning():
        with mpl.rc_context():
            _copy = mpl.rcParams.copy()
            for key in _copy:
                mpl.rcParams[key] = _copy[key]
        with mpl.rc_context():
            copy.deepcopy(mpl.rcParams)
        # real test is that this does not raise
        assert validate_bool_maybe_none(None) is None
        assert validate_bool_maybe_none("none") is None
        with pytest.raises(ValueError):
            validate_bool_maybe_none("blah")
    with pytest.raises(ValueError):
        validate_bool(None)
    with pytest.raises(ValueError):
        with mpl.rc_context():
            mpl.rcParams['svg.fonttype'] = True
