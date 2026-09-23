    @pytest.mark.parametrize('steps, result', [
        ([1, 2, 10], [1, 2, 10]),
        ([2, 10], [1, 2, 10]),
        ([1, 2], [1, 2, 10]),
        ([2], [1, 2, 10]),
    ])
    def test_padding(self, steps, result):
        loc = mticker.MaxNLocator(steps=steps)
        assert (loc._steps == result).all()
