def test_open_files_write(tmpdir):
    tmpdir = str(tmpdir)
    f = open_file_write([os.path.join(tmpdir, 'test1'),
                         os.path.join(tmpdir, 'test2')])
    assert len(f) == 2
    files = compute(*f)
    assert files[0].mode == 'wb'
