@pytest.mark.parametrize('urlpath, expected_path', (
    (r'c:\foo\bar', r'c:\foo\bar'),
    (r'C:\\foo\bar', r'C:\\foo\bar'),
    (r'c:/foo/bar', r'c:/foo/bar'),
    (r'file:///c|\foo\bar', r'c:\foo\bar'),
    (r'file:///C|/foo/bar', r'C:/foo/bar'),
    (r'file:///C:/foo/bar', r'C:/foo/bar'),
))
def test_infer_storage_options_c(urlpath, expected_path):
    so = infer_storage_options(urlpath)
    assert so['protocol'] == 'file'
    assert so['path'] == expected_path
