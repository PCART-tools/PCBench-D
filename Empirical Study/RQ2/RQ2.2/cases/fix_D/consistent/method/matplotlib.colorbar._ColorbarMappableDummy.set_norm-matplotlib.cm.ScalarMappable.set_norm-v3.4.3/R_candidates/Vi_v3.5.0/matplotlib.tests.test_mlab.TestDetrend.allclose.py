    def allclose(self, *args):
        assert_allclose(*args, atol=1e-8)
