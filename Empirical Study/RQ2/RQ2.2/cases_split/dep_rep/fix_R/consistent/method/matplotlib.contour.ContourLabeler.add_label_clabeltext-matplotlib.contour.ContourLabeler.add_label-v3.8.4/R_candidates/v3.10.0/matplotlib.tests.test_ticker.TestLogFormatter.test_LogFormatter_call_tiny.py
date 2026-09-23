    @pytest.mark.parametrize('val', [1e-323, 2e-323, 10e-323, 11e-323])
    def test_LogFormatter_call_tiny(self, val):
        # test coeff computation in __call__
        temp_lf = mticker.LogFormatter()
        temp_lf.create_dummy_axis()
        temp_lf.axis.set_view_interval(1, 10)
        temp_lf(val)
