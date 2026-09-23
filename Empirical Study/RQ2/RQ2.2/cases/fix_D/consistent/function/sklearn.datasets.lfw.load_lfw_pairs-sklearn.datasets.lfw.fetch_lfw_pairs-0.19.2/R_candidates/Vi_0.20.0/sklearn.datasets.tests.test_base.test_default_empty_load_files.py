def test_default_empty_load_files(load_files_root):
    res = load_files(load_files_root)
    assert_equal(len(res.filenames), 0)
    assert_equal(len(res.target_names), 0)
    assert_equal(res.DESCR, None)
