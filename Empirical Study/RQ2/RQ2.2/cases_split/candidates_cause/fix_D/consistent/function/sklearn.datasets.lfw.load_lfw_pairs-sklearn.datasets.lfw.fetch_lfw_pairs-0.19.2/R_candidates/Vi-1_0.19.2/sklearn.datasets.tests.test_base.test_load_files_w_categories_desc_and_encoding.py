@with_setup(setup_load_files, teardown_load_files)
def test_load_files_w_categories_desc_and_encoding():
    category = os.path.abspath(TEST_CATEGORY_DIR1).split('/').pop()
    res = load_files(LOAD_FILES_ROOT, description="test",
                     categories=category, encoding="utf-8")
    assert_equal(len(res.filenames), 1)
    assert_equal(len(res.target_names), 1)
    assert_equal(res.DESCR, "test")
    assert_equal(res.data, [u("Hello World!\n")])
