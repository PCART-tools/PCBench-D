    def test_bad_dims(self):
        data = np.random.normal(size=(34, 34, 34))
        with pytest.raises(ValueError):
            results = cbook.boxplot_stats(data)
