def test_GetFunctionTestMixin_class():
    class TestCustomGetFail(GetFunctionTestMixin):
        get = staticmethod(lambda x, y: 1)

    custom_testget = TestCustomGetFail()
    pytest.raises(AssertionError, custom_testget.test_get)

    class TestCustomGetPass(GetFunctionTestMixin):
        get = staticmethod(core.get)

    custom_testget = TestCustomGetPass()
    custom_testget.test_get()
