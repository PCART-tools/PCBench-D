def insert_to_ooc(out, arr, lock=True):
    if lock is True:
        lock = Lock()

    def store(x, index, lock):
        if lock:
            lock.acquire()
        try:
            out[index] = np.asanyarray(x)
        finally:
            if lock:
                lock.release()

        return None

    slices = slices_from_chunks(arr.chunks)

    name = 'store-%s' % arr.name
    dsk = dict(((name,) + t[1:], (store, t, slc, lock))
               for t, slc in zip(core.flatten(arr._keys()), slices))
    return dsk
