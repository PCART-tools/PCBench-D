    def test_one_half(self):
        """
        Test the parameter one_half
        """
        form = mticker.LogitFormatter()
        assert r"\frac{1}{2}" in form(1/2)
        form.set_one_half("1/2")
        assert "1/2" in form(1/2)
        form.set_one_half("one half")
        assert "one half" in form(1/2)
