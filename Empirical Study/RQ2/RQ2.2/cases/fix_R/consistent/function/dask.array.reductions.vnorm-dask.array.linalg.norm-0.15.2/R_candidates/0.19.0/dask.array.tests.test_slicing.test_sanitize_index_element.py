def test_sanitize_index_element():
    with pytest.raises(TypeError):
        _sanitize_index_element('Hello!')
