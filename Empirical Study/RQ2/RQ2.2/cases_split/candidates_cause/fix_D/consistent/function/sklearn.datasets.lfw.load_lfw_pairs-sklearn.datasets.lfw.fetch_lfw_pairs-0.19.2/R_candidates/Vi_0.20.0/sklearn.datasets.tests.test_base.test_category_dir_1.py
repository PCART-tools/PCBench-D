@pytest.fixture
def test_category_dir_1(load_files_root):
    test_category_dir1 = tempfile.mkdtemp(dir=load_files_root)
    sample_file = tempfile.NamedTemporaryFile(dir=test_category_dir1,
                                              delete=False)
    sample_file.write(b("Hello World!\n"))
    sample_file.close()
    yield str(test_category_dir1)
    _remove_dir(test_category_dir1)
