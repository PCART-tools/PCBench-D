def test_memmap():
    with tmpfile('npy') as fn_1:
        with tmpfile('npy') as fn_2:
            try:
                x = da.arange(100, chunks=15)
                target = np.memmap(fn_1, shape=x.shape, mode='w+', dtype=x.dtype)

                x.store(target)

                assert_eq(target, x)

                np.save(fn_2, target)

                assert_eq(np.load(fn_2, mmap_mode='r'), x)
            finally:
                target._mmap.close()
