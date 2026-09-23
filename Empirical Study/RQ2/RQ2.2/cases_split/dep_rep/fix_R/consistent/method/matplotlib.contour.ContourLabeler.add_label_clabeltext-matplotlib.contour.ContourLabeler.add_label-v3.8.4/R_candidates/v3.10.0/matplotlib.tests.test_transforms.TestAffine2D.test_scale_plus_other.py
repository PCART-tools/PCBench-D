    def test_scale_plus_other(self):
        trans = Affine2D().scale(3, -2).rotate_deg(90)
        trans_added = Affine2D().scale(3, -2) + Affine2D().rotate_deg(90)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_equal(trans.transform(self.single_point), [2, 3])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[4, 0], [6, 9], [0, 12]])

        trans = Affine2D().scale(3, -2).rotate_deg_around(*self.pivot, 90)
        trans_added = (Affine2D().scale(3, -2) +
                       Affine2D().rotate_deg_around(*self.pivot, 90))
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_equal(trans.transform(self.single_point), [4, 3])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[6, 0], [8, 9], [2, 12]])

        trans = (Affine2D().scale(3, -2)
                 .skew_deg(26.5650512, 14.0362435))  # ~atan(0.5), ~atan(0.25)
        trans_added = (Affine2D().scale(3, -2) +
                       Affine2D().skew_deg(26.5650512, 14.0362435))
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [2, -1.25])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[-2, -4], [6, -3.75], [12, 3]])

        trans = Affine2D().scale(3, -2).translate(23, 42)
        trans_added = Affine2D().scale(3, -2) + Affine2D().translate(23, 42)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_equal(trans.transform(self.single_point), [26, 40])
        assert_array_equal(trans.transform(self.multiple_points),
                           [[23, 38], [32, 36], [35, 42]])
