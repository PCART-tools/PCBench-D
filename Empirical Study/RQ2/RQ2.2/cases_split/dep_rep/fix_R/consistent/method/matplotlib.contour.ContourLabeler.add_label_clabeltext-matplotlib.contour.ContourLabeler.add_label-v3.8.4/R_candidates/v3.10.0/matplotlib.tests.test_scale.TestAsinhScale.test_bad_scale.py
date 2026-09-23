    def test_bad_scale(self):
        fig, ax = plt.subplots()

        with pytest.raises(ValueError):
            AsinhScale(axis=None, linear_width=0)
        with pytest.raises(ValueError):
            AsinhScale(axis=None, linear_width=-1)
        s0 = AsinhScale(axis=None, )
        s1 = AsinhScale(axis=None, linear_width=3.0)
