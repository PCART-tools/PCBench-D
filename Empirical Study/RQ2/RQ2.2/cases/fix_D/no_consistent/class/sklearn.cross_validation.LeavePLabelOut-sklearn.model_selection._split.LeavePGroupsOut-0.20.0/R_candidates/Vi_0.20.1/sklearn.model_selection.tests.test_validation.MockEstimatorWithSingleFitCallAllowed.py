class MockEstimatorWithSingleFitCallAllowed(MockEstimatorWithParameter):
    """Dummy classifier that disallows repeated calls of fit method"""

    def fit(self, X_subset, y_subset):
        assert_false(
            hasattr(self, 'fit_called_'),
            'fit is called the second time'
        )
        self.fit_called_ = True
        return super(type(self), self).fit(X_subset, y_subset)

    def predict(self, X):
        raise NotImplementedError
