    def fit(self, X, y, sample_weight=None):
        assert isinstance(X, list)
        return super().fit(X, y, sample_weight)
