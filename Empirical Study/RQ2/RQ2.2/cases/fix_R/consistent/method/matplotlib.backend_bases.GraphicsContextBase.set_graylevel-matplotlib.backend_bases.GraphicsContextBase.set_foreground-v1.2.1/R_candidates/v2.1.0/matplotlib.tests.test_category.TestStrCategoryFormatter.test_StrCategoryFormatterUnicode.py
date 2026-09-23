    def test_StrCategoryFormatterUnicode(self):
        seq = ["Здравствуйте", "привет"]
        labels = cat.StrCategoryFormatter(seq)
        assert labels('a', 1) == "привет"
