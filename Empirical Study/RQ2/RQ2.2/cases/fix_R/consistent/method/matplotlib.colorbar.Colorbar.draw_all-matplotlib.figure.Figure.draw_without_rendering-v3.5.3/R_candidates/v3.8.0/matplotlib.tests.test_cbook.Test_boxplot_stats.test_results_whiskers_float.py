    def test_results_whiskers_float(self):
        results = cbook.boxplot_stats(self.data, whis=3)
        res = results[0]
        for key, value in self.known_whis3_res.items():
            assert_array_almost_equal(res[key], value)
