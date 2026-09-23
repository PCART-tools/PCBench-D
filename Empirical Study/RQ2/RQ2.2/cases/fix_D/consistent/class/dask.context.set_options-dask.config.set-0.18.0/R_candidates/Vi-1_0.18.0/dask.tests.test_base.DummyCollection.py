    class DummyCollection(object):
        def __init__(self, dsk=None):
            self.dask = dsk

        def __dask_graph__(self):
            return self.dask
