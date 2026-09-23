    def test_invalidate(self):
        before = np.array([[1.0, 4.0, 0.0],
                           [5.0, 1.0, 0.0],
                           [0.0, 0.0, 1.0]])
        after = np.array([[1.0, 3.0, 0.0],
                          [5.0, 1.0, 0.0],
                          [0.0, 0.0, 1.0]])

        # Translation and skew present
        base = mtransforms.Affine2D.from_values(1, 5, 4, 1, 2, 3)
        t = mtransforms.AffineDeltaTransform(base)
        assert_array_equal(t.get_matrix(), before)

        # Mess with the internal structure of `base` without invalidating
        # This should not affect this transform because it's a passthrough:
        # it's always invalid
        base.get_matrix()[0, 1:] = 3
        assert_array_equal(t.get_matrix(), after)

        # Invalidate the base
        base.invalidate()
        assert_array_equal(t.get_matrix(), after)
