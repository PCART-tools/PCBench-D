    def test_rotate_around_plus_other(self):
        trans = Affine2D().rotate_deg_around(*self.pivot, 90).rotate_deg(180)
        trans_added = (Affine2D().rotate_deg_around(*self.pivot, 90) +
                       Affine2D().rotate_deg(180))
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [-1, -1])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[0, 0], [1, -3], [-2, -4]])

        trans = Affine2D().rotate_deg_around(*self.pivot, 90).scale(3, -2)
        trans_added = (Affine2D().rotate_deg_around(*self.pivot, 90) +
                       Affine2D().scale(3, -2))
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [3, -2])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[0, 0], [-3, -6], [6, -8]])

        trans = (Affine2D().rotate_deg_around(*self.pivot, 90)
                 .skew_deg(26.5650512, 14.0362435))  # ~atan(0.5), ~atan(0.25)
        trans_added = (Affine2D().rotate_deg_around(*self.pivot, 90) +
                       Affine2D().skew_deg(26.5650512, 14.0362435))
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [1.5, 1.25])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[0, 0], [0.5, 2.75], [4, 4.5]])

        trans = Affine2D().rotate_deg_around(*self.pivot, 90).translate(23, 42)
        trans_added = (Affine2D().rotate_deg_around(*self.pivot, 90) +
                       Affine2D().translate(23, 42))
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [24, 43])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[23, 42], [22, 45], [25, 46]])
