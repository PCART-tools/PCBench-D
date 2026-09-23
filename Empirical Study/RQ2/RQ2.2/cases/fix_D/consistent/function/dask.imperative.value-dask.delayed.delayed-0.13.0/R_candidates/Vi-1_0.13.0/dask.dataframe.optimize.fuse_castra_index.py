def fuse_castra_index(dsk):
    from castra import Castra

    def merge(a, b):
        return (Castra.load_index, b[1], b[2]) if a[2] == 'index' else a
    return fuse_selections(dsk, getattr, Castra.load_partition, merge)
