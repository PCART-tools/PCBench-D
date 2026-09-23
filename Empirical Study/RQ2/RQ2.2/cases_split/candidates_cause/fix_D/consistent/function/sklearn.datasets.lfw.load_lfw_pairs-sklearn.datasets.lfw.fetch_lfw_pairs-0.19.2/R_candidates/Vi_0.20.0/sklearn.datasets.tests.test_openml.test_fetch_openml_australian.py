@pytest.mark.parametrize('gzip_response', [True, False])
def test_fetch_openml_australian(monkeypatch, gzip_response):
    # sparse dataset
    # Australian is the only sparse dataset that is reasonably small
    # as it is inactive, we need to catch the warning. Due to mocking
    # framework, it is not deactivated in our tests
    data_id = 292
    data_name = 'Australian'
    data_version = 1
    target_column = 'Y'
    # Not all original instances included for space reasons
    expected_observations = 85
    expected_features = 14
    expected_missing = 0
    _monkey_patch_webbased_functions(monkeypatch, data_id, gzip_response)
    assert_warns_message(
        UserWarning,
        "Version 1 of dataset Australian is inactive,",
        _fetch_dataset_from_openml,
        **{'data_id': data_id, 'data_name': data_name,
           'data_version': data_version,
           'target_column': target_column,
           'expected_observations': expected_observations,
           'expected_features': expected_features,
           'expected_missing': expected_missing,
           'expect_sparse': True,
           'expected_data_dtype': np.float64,
           'expected_target_dtype': object,
           'compare_default_target': False}  # numpy specific check
    )
