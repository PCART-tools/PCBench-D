def test_from_function_requires_block_args():
    x = np.arange(10)
    pytest.raises(Exception, lambda: from_array(x))
