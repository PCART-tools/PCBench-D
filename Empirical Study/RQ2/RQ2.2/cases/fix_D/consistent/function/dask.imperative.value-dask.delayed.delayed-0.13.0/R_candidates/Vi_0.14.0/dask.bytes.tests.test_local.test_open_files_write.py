def test_open_files_write(tmpdir):
    tmpdir = str(tmpdir)
    files = open_files([os.path.join(tmpdir, 'test1'),
                        os.path.join(tmpdir, 'test2')], mode='wb')
    assert len(files) == 2
    assert files[0].mode == 'wb'
