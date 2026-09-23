class Foo(object):
    @globalmethod(key='f')
    def f():
        return 1

    g = globalmethod(foo, key='g', falsey=bar)
