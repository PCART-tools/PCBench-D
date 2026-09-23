    def test_evaluate_inv_dim(self):
        """ Invert the dimensions. i.e., Give the dataset a dimension of
        1 [3,2,4], and the points will have a dimension of 3 [[3],[2],[4]].
        ValueError should be raised"""
        np.random.seed(8765678)
        n_basesample = 50
        multidim_data = np.random.randn(n_basesample)
        kde = mlab.GaussianKDE(multidim_data)
        x2 = [[1], [2], [3]]
        with pytest.raises(ValueError):
            kde.evaluate(x2)
