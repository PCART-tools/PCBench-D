    class CustomSearchCV(BaseSearchCV):
        def __init__(self, estimator, **kwargs):
            super(CustomSearchCV, self).__init__(estimator, **kwargs)

        def _run_search(self, evaluate):
            results = evaluate([{'max_depth': 1}, {'max_depth': 2}])
            check_results(results, fit_grid({'max_depth': [1, 2]}))
            results = evaluate([{'min_samples_split': 5},
                                {'min_samples_split': 10}])
            check_results(results, fit_grid([{'max_depth': [1, 2]},
                                             {'min_samples_split': [5, 10]}]))
