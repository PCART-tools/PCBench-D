def test_classproperty_deprecation():
    class A:
        @_api.deprecated("0.0.0")
        @_api.classproperty
        def f(cls):
            pass
    with pytest.warns(_api.MatplotlibDeprecationWarning):
        A.f
    with pytest.warns(_api.MatplotlibDeprecationWarning):
        a = A()
        a.f
