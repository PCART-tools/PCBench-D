    def test_values(self):
        np.random.seed(19680801)
        values = np.random.random(6)
        assert_array_equal(Affine2D.from_values(*values).to_values(), values)
