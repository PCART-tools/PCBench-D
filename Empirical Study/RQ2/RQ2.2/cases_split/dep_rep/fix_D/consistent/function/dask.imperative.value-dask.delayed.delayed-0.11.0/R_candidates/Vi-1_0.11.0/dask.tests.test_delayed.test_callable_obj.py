def test_callable_obj():
    class Foo(object):
        def __init__(self, a):
            self.a = a

        def __call__(self):
            return 2

    foo = Foo(1)
    f = delayed(foo)
    assert f.compute() is foo
    assert f.a.compute() == 1
    assert f().compute() == 2
