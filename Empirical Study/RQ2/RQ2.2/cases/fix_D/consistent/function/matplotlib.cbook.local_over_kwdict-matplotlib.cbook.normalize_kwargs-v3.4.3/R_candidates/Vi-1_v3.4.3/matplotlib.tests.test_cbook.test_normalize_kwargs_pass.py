@pytest.mark.parametrize('inp, expected, kwargs_to_norm',
                         pass_mapping)
def test_normalize_kwargs_pass(inp, expected, kwargs_to_norm):
    with _api.suppress_matplotlib_deprecation_warning():
        # No other warning should be emitted.
        assert expected == cbook.normalize_kwargs(inp, **kwargs_to_norm)
