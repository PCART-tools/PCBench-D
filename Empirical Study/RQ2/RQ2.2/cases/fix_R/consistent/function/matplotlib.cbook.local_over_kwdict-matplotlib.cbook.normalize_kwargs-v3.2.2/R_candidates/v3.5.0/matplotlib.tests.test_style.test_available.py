def test_available():
    with temp_style('_test_', DUMMY_SETTINGS):
        assert '_test_' in style.available
