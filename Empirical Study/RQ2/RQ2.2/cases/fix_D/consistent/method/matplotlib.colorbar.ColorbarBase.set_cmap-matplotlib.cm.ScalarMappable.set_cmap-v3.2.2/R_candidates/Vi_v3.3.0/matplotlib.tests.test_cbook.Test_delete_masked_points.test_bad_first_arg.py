    def test_bad_first_arg(self):
        with pytest.raises(ValueError):
            delete_masked_points('a string', np.arange(1.0, 7.0))
