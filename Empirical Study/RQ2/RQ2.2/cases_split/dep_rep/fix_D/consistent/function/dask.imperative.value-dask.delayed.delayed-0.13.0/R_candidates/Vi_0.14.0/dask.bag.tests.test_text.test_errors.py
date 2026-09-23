def test_errors():
    with filetexts({'.test.foo': b'Jos\xe9\nAlice'}, mode='b'):
        with pytest.raises(UnicodeDecodeError):
            read_text('.test.foo', encoding='ascii').compute()

        result = read_text('.test.foo', encoding='ascii', errors='ignore')
        result = result.compute(get=get)
        assert result == ['Jos\n', 'Alice']
