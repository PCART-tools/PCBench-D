@pytest.fixture(scope="module")
def data_home(tmpdir_factory):
    tmp_file = str(tmpdir_factory.mktemp("scikit_learn_data_home_test"))
    yield tmp_file
    _remove_dir(tmp_file)
