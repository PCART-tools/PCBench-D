    def test_clear(self):
        a = Affine2D(np.random.rand(3, 3) + 5)  # Anything non-identity.
        a.clear()
        assert_array_equal(a.get_matrix(), [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
