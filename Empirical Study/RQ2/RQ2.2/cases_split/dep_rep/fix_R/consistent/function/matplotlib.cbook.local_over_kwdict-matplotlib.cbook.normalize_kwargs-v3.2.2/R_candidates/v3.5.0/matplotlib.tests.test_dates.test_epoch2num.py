def test_epoch2num():
    with _api.suppress_matplotlib_deprecation_warning():
        mdates._reset_epoch_test_example()
        mdates.set_epoch('0000-12-31')
        assert mdates.epoch2num(86400) == 719164.0
        assert mdates.num2epoch(719165.0) == 86400 * 2
        # set back to the default
        mdates._reset_epoch_test_example()
        mdates.set_epoch('1970-01-01T00:00:00')
        assert mdates.epoch2num(86400) == 1.0
        assert mdates.num2epoch(2.0) == 86400 * 2
