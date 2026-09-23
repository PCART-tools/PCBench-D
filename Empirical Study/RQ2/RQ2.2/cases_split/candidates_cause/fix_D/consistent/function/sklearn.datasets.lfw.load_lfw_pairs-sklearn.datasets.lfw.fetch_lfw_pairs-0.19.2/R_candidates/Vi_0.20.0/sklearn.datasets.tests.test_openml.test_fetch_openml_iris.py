@pytest.mark.parametrize('gzip_response', [True, False])
def test_fetch_openml_iris(monkeypatch, gzip_response):
    # classification dataset with numeric only columns
    data_id = 61
    data_name = 'iris'
    data_version = 1
    target_column = 'class'
    expected_observations = 150
    expected_features = 4
    expected_missing = 0

    _monkey_patch_webbased_functions(monkeypatch, data_id, gzip_response)
    assert_warns_message(
        UserWarning,
        "Multiple active versions of the dataset matching the name"
        " iris exist. Versions may be fundamentally different, "
        "returning version 1.",
        _fetch_dataset_from_openml,
        **{'data_id': data_id, 'data_name': data_name,
           'data_version': data_version,
           'target_column': target_column,
           'expected_observations': expected_observations,
           'expected_features': expected_features,
           'expected_missing': expected_missing,
           'expect_sparse': False,
           'expected_data_dtype': np.float64,
           'expected_target_dtype': object,
           'compare_default_target': True}
    )
