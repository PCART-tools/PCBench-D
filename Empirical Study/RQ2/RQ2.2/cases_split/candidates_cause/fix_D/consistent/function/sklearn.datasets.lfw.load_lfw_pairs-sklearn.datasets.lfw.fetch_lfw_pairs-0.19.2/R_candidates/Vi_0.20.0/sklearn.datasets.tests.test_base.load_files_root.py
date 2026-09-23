@pytest.fixture(scope="module")
def load_files_root(tmpdir_factory):
    tmp_file = str(tmpdir_factory.mktemp("scikit_learn_load_files_test"))
    yield tmp_file
    _remove_dir(tmp_file)
