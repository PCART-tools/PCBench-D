class TestRecursiveGet(GetFunctionTestMixin):
    get = staticmethod(lambda d, k: core.get(d, k, recursive=True))

    def test_get_stack_limit(self):
        # will blow stack in recursive mode
        pass
