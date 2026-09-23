@pytest.mark.parametrize('gzip_response', [True, False])
def test_raises_illegal_multitarget(monkeypatch, gzip_response):
    data_id = 61
    targets = ['sepalwidth', 'class']
    _monkey_patch_webbased_functions(monkeypatch, data_id, gzip_response)
    # Note that we only want to search by name (not data id)
    assert_raise_message(ValueError,
                         "Can only handle homogeneous multi-target datasets,",
                         fetch_openml, data_id=data_id,
                         target_column=targets, cache=False)
