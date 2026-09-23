def mock_wrapper(method):
    mock = MagicMock()

    def wrapper(self, *args, **kwargs):
        mock(*args, **kwargs)
        return method(self, *args, **kwargs)
    wrapper.mock = mock
    return wrapper
