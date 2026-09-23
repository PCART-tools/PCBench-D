    def test_StrCategoryFormatter(self):
        seq = ["hello", "world", "hi"]
        labels = cat.StrCategoryFormatter(seq)
        assert labels('a', 1) == "world"
