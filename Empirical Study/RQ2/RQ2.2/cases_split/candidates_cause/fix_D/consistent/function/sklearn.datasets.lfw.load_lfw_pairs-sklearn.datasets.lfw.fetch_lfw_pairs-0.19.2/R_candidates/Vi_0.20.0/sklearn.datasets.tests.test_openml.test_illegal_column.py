@pytest.mark.parametrize('gzip_response', [True, False])
def test_illegal_column(monkeypatch, gzip_response):
    data_id = 61
    _monkey_patch_webbased_functions(monkeypatch, data_id, gzip_response)
    assert_raise_message(KeyError, "Could not find target_column=",
                         fetch_openml, data_id=data_id,
                         target_column='undefined', cache=False)

    assert_raise_message(KeyError, "Could not find target_column=",
                         fetch_openml, data_id=data_id,
                         target_column=['undefined', 'class'],
                         cache=False)
