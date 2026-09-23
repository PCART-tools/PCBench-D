    def test_rotate(self):
        r_pi_2 = Affine2D().rotate(np.pi / 2)
        r90 = Affine2D().rotate_deg(90)
        assert_array_equal(r_pi_2.get_matrix(), r90.get_matrix())
        assert_array_almost_equal(r90.transform(self.single_point), [-1, 1])
        assert_array_almost_equal(r90.transform(self.multiple_points),
                                  [[-2, 0], [-3, 3], [0, 4]])

        r_pi = Affine2D().rotate(np.pi)
        r180 = Affine2D().rotate_deg(180)
        assert_array_equal(r_pi.get_matrix(), r180.get_matrix())
        assert_array_almost_equal(r180.transform(self.single_point), [-1, -1])
        assert_array_almost_equal(r180.transform(self.multiple_points),
                                  [[0, -2], [-3, -3], [-4, 0]])

        r_pi_3_2 = Affine2D().rotate(3 * np.pi / 2)
        r270 = Affine2D().rotate_deg(270)
        assert_array_equal(r_pi_3_2.get_matrix(), r270.get_matrix())
        assert_array_almost_equal(r270.transform(self.single_point), [1, -1])
        assert_array_almost_equal(r270.transform(self.multiple_points),
                                  [[2, 0], [3, -3], [0, -4]])

        assert_array_equal((r90 + r90).get_matrix(), r180.get_matrix())
        assert_array_equal((r90 + r180).get_matrix(), r270.get_matrix())
