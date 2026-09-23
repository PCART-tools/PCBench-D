def test_simple_write(tmpdir):
    tmpdir = str(tmpdir)
    make_bytes = lambda: b'000'
    some_bytes = delayed(make_bytes)()
    data = [some_bytes, some_bytes]
    out = write_bytes(data, tmpdir)
    assert len(out) == 2
    compute(*out)
    files = os.listdir(tmpdir)
    assert len(files) == 2
    assert '0.part' in files
    d = open(os.path.join(tmpdir, files[0]), 'rb').read()
    assert d == b'000'
