    class TestCustomGetFail(GetFunctionTestMixin):
        get = staticmethod(lambda x, y: 1)
