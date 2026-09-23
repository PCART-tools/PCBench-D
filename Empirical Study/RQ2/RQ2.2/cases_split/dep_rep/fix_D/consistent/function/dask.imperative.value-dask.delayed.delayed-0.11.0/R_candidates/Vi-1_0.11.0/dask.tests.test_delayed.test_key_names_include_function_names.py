def test_key_names_include_function_names():
    def myfunc(x):
        return x + 1
    assert delayed(myfunc)(1).key.startswith('myfunc')
