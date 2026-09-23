@pytest.mark.parametrize('gzip_response', [True, False])
def test_string_attribute(monkeypatch, gzip_response):
    data_id = 40945
    _monkey_patch_webbased_functions(monkeypatch, data_id, gzip_response)
    # single column test
    assert_raise_message(ValueError,
                         'STRING attributes are not yet supported',
                         fetch_openml, data_id=data_id, cache=False)
