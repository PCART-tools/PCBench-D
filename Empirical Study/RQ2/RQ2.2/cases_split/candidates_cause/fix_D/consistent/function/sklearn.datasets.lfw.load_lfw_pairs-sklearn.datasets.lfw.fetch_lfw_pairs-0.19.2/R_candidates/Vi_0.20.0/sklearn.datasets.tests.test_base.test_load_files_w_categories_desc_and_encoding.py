def test_load_files_w_categories_desc_and_encoding(
        test_category_dir_1, test_category_dir_2, load_files_root):
    category = os.path.abspath(test_category_dir_1).split('/').pop()
    res = load_files(load_files_root, description="test",
                     categories=category, encoding="utf-8")
    assert_equal(len(res.filenames), 1)
    assert_equal(len(res.target_names), 1)
    assert_equal(res.DESCR, "test")
    assert_equal(res.data, [u("Hello World!\n")])
