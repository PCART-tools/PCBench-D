    def test_results_whiskers_range(self):
        results = cbook.boxplot_stats(self.data, whis=[0, 100])
        res = results[0]
        for key, value in self.known_res_range.items():
            assert_array_almost_equal(res[key], value)
