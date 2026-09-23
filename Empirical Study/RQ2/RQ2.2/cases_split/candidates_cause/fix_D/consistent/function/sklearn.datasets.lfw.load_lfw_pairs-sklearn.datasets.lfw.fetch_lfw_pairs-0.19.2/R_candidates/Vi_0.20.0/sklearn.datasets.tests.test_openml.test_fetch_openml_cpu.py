@pytest.mark.parametrize('gzip_response', [True, False])
def test_fetch_openml_cpu(monkeypatch, gzip_response):
    # regression dataset with numeric and categorical columns
    data_id = 561
    data_name = 'cpu'
    data_version = 1
    target_column = 'class'
    expected_observations = 209
    expected_features = 7
    expected_missing = 0
    _monkey_patch_webbased_functions(monkeypatch, data_id, gzip_response)
    _fetch_dataset_from_openml(data_id, data_name, data_version, target_column,
                               expected_observations, expected_features,
                               expected_missing,
                               object, np.float64, expect_sparse=False,
                               compare_default_target=True)
