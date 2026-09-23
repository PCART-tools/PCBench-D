    def test_label_error(self):
        labels = [1, 2]
        with pytest.raises(ValueError):
            cbook.boxplot_stats(self.data, labels=labels)
