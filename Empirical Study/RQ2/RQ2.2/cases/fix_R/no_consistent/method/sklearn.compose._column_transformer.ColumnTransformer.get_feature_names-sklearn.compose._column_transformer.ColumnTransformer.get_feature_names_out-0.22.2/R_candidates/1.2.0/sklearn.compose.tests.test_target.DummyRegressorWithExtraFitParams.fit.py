    def fit(self, X, y, sample_weight=None, check_input=True):
        # on the test below we force this to false, we make sure this is
        # actually passed to the regressor
        assert not check_input
        return super().fit(X, y, sample_weight)
