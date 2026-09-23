class TestIndexFormatter:
    @pytest.mark.parametrize('x, label', [(-2, ''),
                                          (-1, 'label0'),
                                          (0, 'label0'),
                                          (0.5, 'label1'),
                                          (1, 'label1'),
                                          (1.5, 'label2'),
                                          (2, 'label2'),
                                          (2.5, '')])
    def test_formatting(self, x, label):
        with _api.suppress_matplotlib_deprecation_warning():
            formatter = mticker.IndexFormatter(['label0', 'label1', 'label2'])
        assert formatter(x) == label
