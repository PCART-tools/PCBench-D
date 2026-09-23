    class Foo(object):
        def __init__(self, x):
            self.x = x

        def __dask_tokenize__(self):
            return self.x
