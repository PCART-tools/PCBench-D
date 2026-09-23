@pytest.mark.parametrize('inp, kwargs_to_norm', fail_mapping)
def test_normalize_kwargs_fail(inp, kwargs_to_norm):
    with pytest.raises(TypeError), \
         _api.suppress_matplotlib_deprecation_warning():
        cbook.normalize_kwargs(inp, **kwargs_to_norm)
