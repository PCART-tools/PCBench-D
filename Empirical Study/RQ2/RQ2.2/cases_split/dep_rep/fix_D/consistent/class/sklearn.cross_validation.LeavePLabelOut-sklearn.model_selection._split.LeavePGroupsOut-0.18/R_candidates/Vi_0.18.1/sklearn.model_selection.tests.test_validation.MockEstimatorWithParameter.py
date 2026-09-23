class MockEstimatorWithParameter(BaseEstimator):
    """Dummy classifier to test the validation curve"""
    def __init__(self, param=0.5):
        self.X_subset = None
        self.param = param

    def fit(self, X_subset, y_subset):
        self.X_subset = X_subset
        self.train_sizes = X_subset.shape[0]
        return self

    def predict(self, X):
        raise NotImplementedError

    def score(self, X=None, y=None):
        return self.param if self._is_training_data(X) else 1 - self.param

    def _is_training_data(self, X):
        return X is self.X_subset
