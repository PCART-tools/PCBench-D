def test_deprecate_privatize_attribute():
    class C:
        def __init__(self): self._attr = 1
        def _meth(self, arg): return arg
        attr = _api.deprecate_privatize_attribute("0.0")
        meth = _api.deprecate_privatize_attribute("0.0")

    c = C()
    with pytest.warns(_api.MatplotlibDeprecationWarning):
        assert c.attr == 1
    with pytest.warns(_api.MatplotlibDeprecationWarning):
        c.attr = 2
    with pytest.warns(_api.MatplotlibDeprecationWarning):
        assert c.attr == 2
    with pytest.warns(_api.MatplotlibDeprecationWarning):
        assert c.meth(42) == 42
