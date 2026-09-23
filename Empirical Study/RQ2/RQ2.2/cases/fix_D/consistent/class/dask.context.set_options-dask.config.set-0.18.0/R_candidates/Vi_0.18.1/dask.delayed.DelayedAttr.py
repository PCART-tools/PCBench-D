class DelayedAttr(Delayed):
    __slots__ = ('_obj', '_attr', '_key')

    def __init__(self, obj, attr):
        self._obj = obj
        self._attr = attr
        self._key = 'getattr-%s' % tokenize(obj, attr, pure=True)

    @property
    def dask(self):
        dsk = {self._key: (getattr, self._obj._key, self._attr)}
        return sharedict.merge(self._obj.dask, (self._key, dsk))

    def __call__(self, *args, **kwargs):
        return call_function(methodcaller(self._attr), self._attr, (self._obj,) + args, kwargs)
