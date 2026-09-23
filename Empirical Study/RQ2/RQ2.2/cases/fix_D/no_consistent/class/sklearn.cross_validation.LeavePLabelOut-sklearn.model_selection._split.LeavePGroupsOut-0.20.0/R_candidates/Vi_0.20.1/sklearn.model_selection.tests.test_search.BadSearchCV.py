    class BadSearchCV(BaseSearchCV):
        def __init__(self, estimator, **kwargs):
            super(BadSearchCV, self).__init__(estimator, **kwargs)
