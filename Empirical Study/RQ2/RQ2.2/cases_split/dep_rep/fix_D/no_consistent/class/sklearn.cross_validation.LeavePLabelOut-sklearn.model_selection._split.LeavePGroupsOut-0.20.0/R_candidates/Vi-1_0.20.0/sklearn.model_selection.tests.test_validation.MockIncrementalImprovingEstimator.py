class MockIncrementalImprovingEstimator(MockImprovingEstimator):
    """Dummy classifier that provides partial_fit"""
    def __init__(self, n_max_train_sizes):
        super(MockIncrementalImprovingEstimator,
              self).__init__(n_max_train_sizes)
        self.x = None

    def _is_training_data(self, X):
        return self.x in X

    def partial_fit(self, X, y=None, **params):
        self.train_sizes += X.shape[0]
        self.x = X[0]
