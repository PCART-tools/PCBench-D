    def test_results_withlabels(self):
        labels = ['Test1', 2, 'ardvark', 4]
        results = cbook.boxplot_stats(self.data, labels=labels)
        res = results[0]
        for lab, res in zip(labels, results):
            assert res['label'] == lab

        results = cbook.boxplot_stats(self.data)
        for res in results:
            assert 'label' not in res
