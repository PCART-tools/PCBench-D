    def test_rotate_around(self):
        r_pi_2 = Affine2D().rotate_around(*self.pivot, np.pi / 2)
        r90 = Affine2D().rotate_deg_around(*self.pivot, 90)
        assert_array_equal(r_pi_2.get_matrix(), r90.get_matrix())
        assert_array_almost_equal(r90.transform(self.single_point), [1, 1])
        assert_array_almost_equal(r90.transform(self.multiple_points),
                                  [[0, 0], [-1, 3], [2, 4]])

        r_pi = Affine2D().rotate_around(*self.pivot, np.pi)
        r180 = Affine2D().rotate_deg_around(*self.pivot, 180)
        assert_array_equal(r_pi.get_matrix(), r180.get_matrix())
        assert_array_almost_equal(r180.transform(self.single_point), [1, 1])
        assert_array_almost_equal(r180.transform(self.multiple_points),
                                  [[2, 0], [-1, -1], [-2, 2]])

        r_pi_3_2 = Affine2D().rotate_around(*self.pivot, 3 * np.pi / 2)
        r270 = Affine2D().rotate_deg_around(*self.pivot, 270)
        assert_array_equal(r_pi_3_2.get_matrix(), r270.get_matrix())
        assert_array_almost_equal(r270.transform(self.single_point), [1, 1])
        assert_array_almost_equal(r270.transform(self.multiple_points),
                                  [[2, 2], [3, -1], [0, -2]])

        assert_array_almost_equal((r90 + r90).get_matrix(), r180.get_matrix())
        assert_array_almost_equal((r90 + r180).get_matrix(), r270.get_matrix())
