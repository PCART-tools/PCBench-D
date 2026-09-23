def test_compressed_write(tmpdir):
    tmpdir = str(tmpdir)
    make_bytes = lambda: b'000'
    some_bytes = delayed(make_bytes)()
    data = [some_bytes, some_bytes]
    out = write_bytes(data, os.path.join(tmpdir, 'bytes-*.gz'),
                      compression='gzip')
    compute(*out)
    files = os.listdir(tmpdir)
    assert len(files) == 2
    assert 'bytes-0.gz' in files
    import gzip
    d = gzip.GzipFile(os.path.join(tmpdir, files[0])).read()
    assert d == b'000'
