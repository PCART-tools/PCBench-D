def test_py2_local_bytes(tmpdir):
    fn = str(tmpdir / 'myfile.txt.gz')
    with gzip.open(fn, mode='wb') as f:
        f.write(b'hello\nworld')

    ofc = OpenFileCreator(fn, text=True, open=open, mode='rt',
                          compression='gzip', encoding='utf-8')
    lazy_file = ofc(fn)

    with lazy_file as f:
        assert all(isinstance(line, unicode) for line in f)
