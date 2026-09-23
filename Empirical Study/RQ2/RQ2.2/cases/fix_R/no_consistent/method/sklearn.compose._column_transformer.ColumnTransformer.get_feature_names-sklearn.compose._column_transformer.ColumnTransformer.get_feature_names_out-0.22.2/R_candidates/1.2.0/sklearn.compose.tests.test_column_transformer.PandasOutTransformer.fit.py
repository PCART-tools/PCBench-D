    def fit(self, X, y=None):
        pd = pytest.importorskip("pandas")
        assert isinstance(X, pd.DataFrame)
        return self
