@with_setup(setup_load_files, teardown_load_files)
def test_load_files_wo_load_content():
    res = load_files(LOAD_FILES_ROOT, load_content=False)
    assert_equal(len(res.filenames), 1)
    assert_equal(len(res.target_names), 2)
    assert_equal(res.DESCR, None)
    assert_equal(res.get('data'), None)
