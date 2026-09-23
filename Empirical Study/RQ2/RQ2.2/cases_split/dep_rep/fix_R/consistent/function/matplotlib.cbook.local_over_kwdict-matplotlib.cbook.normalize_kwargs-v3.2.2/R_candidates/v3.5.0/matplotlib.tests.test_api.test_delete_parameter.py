def test_delete_parameter():
    @_api.delete_parameter("3.0", "foo")
    def func1(foo=None):
        pass

    @_api.delete_parameter("3.0", "foo")
    def func2(**kwargs):
        pass

    for func in [func1, func2]:
        func()  # No warning.
        with pytest.warns(_api.MatplotlibDeprecationWarning):
            func(foo="bar")

    def pyplot_wrapper(foo=_api.deprecation._deprecated_parameter):
        func1(foo)

    pyplot_wrapper()  # No warning.
    with pytest.warns(_api.MatplotlibDeprecationWarning):
        func(foo="bar")
