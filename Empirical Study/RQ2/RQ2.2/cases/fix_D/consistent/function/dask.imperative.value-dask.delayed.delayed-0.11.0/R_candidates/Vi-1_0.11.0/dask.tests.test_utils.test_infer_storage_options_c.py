def test_infer_storage_options_c():
    so = infer_storage_options(r'c:\foo\bar')
    assert so['protocol'] == 'file'
