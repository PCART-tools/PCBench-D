    def test_bad_first_arg(self):
        with pytest.raises(ValueError):
            dmp('a string', self.arr0)
