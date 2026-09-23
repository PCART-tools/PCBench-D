    def test_evaluate_point_dim_not_one(self):
        x1 = np.arange(3, 10, 2)
        x2 = [np.arange(3, 10, 2), np.arange(3, 10, 2)]
        kde = mlab.GaussianKDE(x1)
        with pytest.raises(ValueError):
            kde.evaluate(x2)
