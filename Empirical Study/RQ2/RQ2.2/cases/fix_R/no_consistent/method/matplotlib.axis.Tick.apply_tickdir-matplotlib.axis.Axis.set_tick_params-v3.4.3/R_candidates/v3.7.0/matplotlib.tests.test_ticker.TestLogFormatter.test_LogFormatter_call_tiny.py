    @pytest.mark.parametrize('val', [1e-323, 2e-323, 10e-323, 11e-323])
    def test_LogFormatter_call_tiny(self, val):
        # test coeff computation in __call__
        temp_lf = mticker.LogFormatter()
        temp_lf.axis = FakeAxis()
        temp_lf(val)
