def test_default_empty_load_files():
    res = load_files(LOAD_FILES_ROOT)
    assert_equal(len(res.filenames), 0)
    assert_equal(len(res.target_names), 0)
    assert_equal(res.DESCR, None)
