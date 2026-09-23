def data(func, dataname, *a, **kw):
    kw.setdefault('dataname', dataname)
    return FuncData(func, DATASETS_BOOST[dataname], *a, **kw)
