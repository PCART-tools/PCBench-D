@pytest.mark.parametrize('gzip_response', [True, False])
def test_open_openml_url_cache(monkeypatch, gzip_response):
    data_id = 61

    _monkey_patch_webbased_functions(
        monkeypatch, data_id, gzip_response)
    openml_path = sklearn.datasets.openml._DATA_FILE.format(data_id)
    test_directory = os.path.join(os.path.expanduser('~'), 'scikit_learn_data')
    # first fill the cache
    response1 = _open_openml_url(openml_path, test_directory)
    # assert file exists
    location = os.path.join(test_directory, 'openml.org', openml_path + '.gz')
    assert os.path.isfile(location)
    # redownload, to utilize cache
    response2 = _open_openml_url(openml_path, test_directory)
    assert response1.read() == response2.read()
