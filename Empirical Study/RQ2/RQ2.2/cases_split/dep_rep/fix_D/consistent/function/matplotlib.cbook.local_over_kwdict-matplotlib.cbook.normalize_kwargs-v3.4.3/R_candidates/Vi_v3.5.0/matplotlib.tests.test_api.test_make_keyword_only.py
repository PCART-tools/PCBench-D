def test_make_keyword_only():
    @_api.make_keyword_only("3.0", "arg")
    def func(pre, arg, post=None):
        pass

    func(1, arg=2)  # Check that no warning is emitted.

    with pytest.warns(_api.MatplotlibDeprecationWarning):
        func(1, 2)
    with pytest.warns(_api.MatplotlibDeprecationWarning):
        func(1, 2, 3)
