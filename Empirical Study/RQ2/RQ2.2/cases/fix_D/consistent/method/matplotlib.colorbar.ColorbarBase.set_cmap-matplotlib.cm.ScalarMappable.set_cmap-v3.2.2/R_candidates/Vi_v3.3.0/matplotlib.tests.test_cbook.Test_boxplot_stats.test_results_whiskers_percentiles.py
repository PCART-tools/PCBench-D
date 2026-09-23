    def test_results_whiskers_percentiles(self):
        results = cbook.boxplot_stats(self.data, whis=[5, 95])
        res = results[0]
        for key, value in self.known_res_percentiles.items():
            assert_array_almost_equal(res[key], value)
