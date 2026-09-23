def test_align_chunks_to_previous_chunks():
    chunks = normalize_chunks('auto',
                              shape=(2000,),
                              previous_chunks=(512,),
                              limit='600 B', dtype=np.uint8)
    assert chunks == ((512, 512, 512, 2000 - 512 * 3),)

    chunks = normalize_chunks('auto',
                              shape=(2000,),
                              previous_chunks=(128,),
                              limit='600 B', dtype=np.uint8)
    assert chunks == ((512, 512, 512, 2000 - 512 * 3),)

    chunks = normalize_chunks('auto',
                              shape=(2000,),
                              previous_chunks=(512,),
                              limit='1200 B', dtype=np.uint8)
    assert chunks == ((1024, 2000 - 1024),)

    chunks = normalize_chunks('auto',
                              shape=(3, 10211, 10376),
                              previous_chunks=(1, 512, 512),
                              limit='1MiB', dtype=np.float32)
    assert chunks[0] == (1, 1, 1)
    assert all(c % 512 == 0 for c in chunks[1][:-1])
    assert all(c % 512 == 0 for c in chunks[2][:-1])
