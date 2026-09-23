    def test_form_each_dict(self):
        for res in self.std_results:
            assert isinstance(res, dict)
