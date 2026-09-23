    def test_string_parser(self):
        normalize = Figure._normalize_grid_string

        assert normalize('ABC') == [['A', 'B', 'C']]
        assert normalize('AB;CC') == [['A', 'B'], ['C', 'C']]
        assert normalize('AB;CC;DE') == [['A', 'B'], ['C', 'C'], ['D', 'E']]
        assert normalize("""
                         ABC
                         """) == [['A', 'B', 'C']]
        assert normalize("""
                         AB
                         CC
                         """) == [['A', 'B'], ['C', 'C']]
        assert normalize("""
                         AB
                         CC
                         DE
                         """) == [['A', 'B'], ['C', 'C'], ['D', 'E']]
