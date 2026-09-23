    class NoRunSearchSearchCV(BaseSearchCV):
        def __init__(self, estimator, **kwargs):
            super(NoRunSearchSearchCV, self).__init__(estimator, **kwargs)

        def fit(self, X, y=None, groups=None, **fit_params):
            return self
