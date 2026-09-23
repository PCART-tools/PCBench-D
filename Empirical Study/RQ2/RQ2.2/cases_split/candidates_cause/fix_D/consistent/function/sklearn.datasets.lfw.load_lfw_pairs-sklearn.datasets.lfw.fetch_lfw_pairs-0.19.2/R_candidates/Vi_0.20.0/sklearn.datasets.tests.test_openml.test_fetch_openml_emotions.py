@pytest.mark.parametrize('gzip_response', [True, False])
def test_fetch_openml_emotions(monkeypatch, gzip_response):
    # classification dataset with multiple targets (natively)
    data_id = 40589
    data_name = 'emotions'
    data_version = 3
    target_column = ['amazed.suprised', 'happy.pleased', 'relaxing.calm',
                     'quiet.still', 'sad.lonely', 'angry.aggresive']
    expected_observations = 13
    expected_features = 72
    expected_missing = 0
    _monkey_patch_webbased_functions(monkeypatch, data_id, gzip_response)

    _fetch_dataset_from_openml(data_id, data_name, data_version, target_column,
                               expected_observations, expected_features,
                               expected_missing,
                               np.float64, object, expect_sparse=False,
                               compare_default_target=True)
