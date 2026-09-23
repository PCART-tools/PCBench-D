    def test_results_baseline(self):
        res = self.std_results[0]
        for key, value in self.known_nonbootstrapped_res.items():
            assert_array_almost_equal(res[key], value)
