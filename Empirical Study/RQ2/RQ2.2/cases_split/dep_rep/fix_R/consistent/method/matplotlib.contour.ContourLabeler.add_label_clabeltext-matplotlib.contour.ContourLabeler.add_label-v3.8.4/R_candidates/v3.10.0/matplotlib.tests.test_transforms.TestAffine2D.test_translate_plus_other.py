    def test_translate_plus_other(self):
        trans = Affine2D().translate(23, 42).rotate_deg(90)
        trans_added = Affine2D().translate(23, 42) + Affine2D().rotate_deg(90)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [-43, 24])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[-44, 23], [-45, 26], [-42, 27]])

        trans = Affine2D().translate(23, 42).rotate_deg_around(*self.pivot, 90)
        trans_added = (Affine2D().translate(23, 42) +
                       Affine2D().rotate_deg_around(*self.pivot, 90))
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [-41, 24])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[-42, 23], [-43, 26], [-40, 27]])

        trans = Affine2D().translate(23, 42).scale(3, -2)
        trans_added = Affine2D().translate(23, 42) + Affine2D().scale(3, -2)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [72, -86])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[69, -88], [78, -90], [81, -84]])

        trans = (Affine2D().translate(23, 42)
                 .skew_deg(26.5650512, 14.0362435))  # ~atan(0.5), ~atan(0.25)
        trans_added = (Affine2D().translate(23, 42) +
                       Affine2D().skew_deg(26.5650512, 14.0362435))
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [45.5, 49])
        assert_array_almost_equal(trans.transform(self.multiple_points),
                                  [[45, 49.75], [48.5, 51.5], [48, 48.75]])
