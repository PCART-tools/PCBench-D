def test_load_files_wo_load_content(
        test_category_dir_1, test_category_dir_2, load_files_root):
    res = load_files(load_files_root, load_content=False)
    assert_equal(len(res.filenames), 1)
    assert_equal(len(res.target_names), 2)
    assert_equal(res.DESCR, None)
    assert_equal(res.get('data'), None)
