    def test_init(self):
        Affine2D([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        Affine2D(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], int))
        Affine2D(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], float))
