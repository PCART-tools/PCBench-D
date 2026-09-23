    def test_modify_inplace(self):
        # Some polar transforms require modifying the matrix in place.
        trans = Affine2D()
        mtx = trans.get_matrix()
        mtx[0, 0] = 42
        assert_array_equal(trans.get_matrix(), [[42, 0, 0], [0, 1, 0], [0, 0, 1]])
