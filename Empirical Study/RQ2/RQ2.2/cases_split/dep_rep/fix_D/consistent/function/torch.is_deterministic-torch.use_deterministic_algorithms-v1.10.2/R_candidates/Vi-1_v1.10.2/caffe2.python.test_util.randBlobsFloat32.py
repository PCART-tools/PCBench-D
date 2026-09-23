def randBlobsFloat32(names, *dims, **kwargs):
    for name in names:
        randBlobFloat32(name, *dims, **kwargs)
