    def test_rotate_plus_other(self):
        trans = Affine2D().rotate_deg(90).rotate_deg_around(*self.pivot, 180)
        trans_added = (Affine2D().rotate_deg(90) +
                       Affine2D().rotate_deg_around(*self.pivot, 180))
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [3, 1])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[4, 2], [5, -1], [2, -2]])

        trans = Affine2D().rotate_deg(90).scale(3, -2)
        trans_added = Affine2D().rotate_deg(90) + Affine2D().scale(3, -2)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [-3, -2])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[-6, -0], [-9, -6], [0, -8]])

        trans = (Affine2D().rotate_deg(90)
                 .skew_deg(26.5650512, 14.0362435))  # ~atan(0.5), ~atan(0.25)
        trans_added = (Affine2D().rotate_deg(90) +
                       Affine2D().skew_deg(26.5650512, 14.0362435))
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [-0.5, 0.75])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[-2, -0.5], [-1.5, 2.25], [2, 4]])

        trans = Affine2D().rotate_deg(90).translate(23, 42)
        trans_added = Affine2D().rotate_deg(90) + Affine2D().translate(23, 42)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [22, 43])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[21, 42], [20, 45], [23, 46]])
