def test_fuse_getitem():
    def load(*args):
        pass
    dsk = {'x': (load, 'store', 'part', ['a', 'b']),
           'y': (getitem, 'x', 'a')}
    dsk2 = fuse_getitem(dsk, load, 3)
    dsk2, dependencies = cull(dsk2, 'y')
    assert dsk2 == {'y': (load, 'store', 'part', 'a')}
