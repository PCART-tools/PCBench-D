def insert_to_ooc(out, arr, lock=True, region=None):
    if lock is True:
        lock = Lock()

    def store(x, index, lock, region):
        if lock:
            lock.acquire()
        try:
            if region is None:
                out[index] = np.asanyarray(x)
            else:
                out[fuse_slice(region, index)] = np.asanyarray(x)
        finally:
            if lock:
                lock.release()

        return None

    slices = slices_from_chunks(arr.chunks)

    name = 'store-%s' % arr.name
    dsk = dict(((name,) + t[1:], (store, t, slc, lock, region))
               for t, slc in zip(core.flatten(arr._keys()), slices))
    return dsk
