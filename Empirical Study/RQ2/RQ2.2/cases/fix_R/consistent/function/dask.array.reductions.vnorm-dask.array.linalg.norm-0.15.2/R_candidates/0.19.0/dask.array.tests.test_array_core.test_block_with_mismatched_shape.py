def test_block_with_mismatched_shape():
    a = np.array([0, 0])
    b = np.eye(2)

    for arrays in [[a, b],
                   [b, a]]:
        with pytest.raises(ValueError):
            da.block(arrays)
