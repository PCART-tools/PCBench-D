    def test_results_bootstrapped(self):
        results = cbook.boxplot_stats(self.data, bootstrap=10000)
        res = results[0]
        for key, value in self.known_bootstrapped_ci.items():
            assert_approx_equal(res[key], value)
