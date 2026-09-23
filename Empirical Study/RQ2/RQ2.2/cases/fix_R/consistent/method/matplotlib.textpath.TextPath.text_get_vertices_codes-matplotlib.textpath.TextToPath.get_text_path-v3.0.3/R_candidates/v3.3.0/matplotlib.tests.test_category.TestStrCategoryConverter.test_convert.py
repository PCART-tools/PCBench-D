    @pytest.mark.parametrize("vals", values, ids=ids)
    def test_convert(self, vals):
        np.testing.assert_allclose(self.cc.convert(vals, self.ax.units,
                                                   self.ax),
                                   range(len(vals)))
