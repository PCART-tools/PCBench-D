    def test_skew_plus_other(self):
        # Using ~atan(0.5), ~atan(0.25) produces roundish numbers on output.
        trans = Affine2D().skew_deg(26.5650512, 14.0362435).rotate_deg(90)
        trans_added = (Affine2D().skew_deg(26.5650512, 14.0362435) +
                       Affine2D().rotate_deg(90))
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [-1.25, 1.5])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[-2, 1], [-3.75, 4.5], [-1, 4]])

        trans = (Affine2D().skew_deg(26.5650512, 14.0362435)
                 .rotate_deg_around(*self.pivot, 90))
        trans_added = (Affine2D().skew_deg(26.5650512, 14.0362435) +
                       Affine2D().rotate_deg_around(*self.pivot, 90))
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [0.75, 1.5])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[0, 1], [-1.75, 4.5], [1, 4]])

        trans = Affine2D().skew_deg(26.5650512, 14.0362435).scale(3, -2)
        trans_added = (Affine2D().skew_deg(26.5650512, 14.0362435) +
                       Affine2D().scale(3, -2))
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [4.5, -2.5])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[3, -4], [13.5, -7.5], [12, -2]])

        trans = Affine2D().skew_deg(26.5650512, 14.0362435).translate(23, 42)
        trans_added = (Affine2D().skew_deg(26.5650512, 14.0362435) +
                       Affine2D().translate(23, 42))
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [24.5, 43.25])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[24, 44], [27.5, 45.75], [27, 43]])
