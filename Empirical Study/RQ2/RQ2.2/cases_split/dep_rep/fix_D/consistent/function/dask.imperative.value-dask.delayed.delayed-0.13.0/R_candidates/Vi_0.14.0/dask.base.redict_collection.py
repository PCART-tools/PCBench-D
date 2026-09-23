def redict_collection(c, dsk):
    cc = copy.copy(c)
    cc.dask = dsk
    return cc
