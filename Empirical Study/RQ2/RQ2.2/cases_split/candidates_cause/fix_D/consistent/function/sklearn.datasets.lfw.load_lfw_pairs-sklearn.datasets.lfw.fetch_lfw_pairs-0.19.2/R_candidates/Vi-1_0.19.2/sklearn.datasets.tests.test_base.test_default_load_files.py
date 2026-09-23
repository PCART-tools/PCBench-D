@with_setup(setup_load_files, teardown_load_files)
def test_default_load_files():
    res = load_files(LOAD_FILES_ROOT)
    assert_equal(len(res.filenames), 1)
    assert_equal(len(res.target_names), 2)
    assert_equal(res.DESCR, None)
    assert_equal(res.data, [b("Hello World!\n")])
