    @pytest.fixture(autouse=True)
    def stride_is_deprecated(self):
        with _api.suppress_matplotlib_deprecation_warning():
            yield
