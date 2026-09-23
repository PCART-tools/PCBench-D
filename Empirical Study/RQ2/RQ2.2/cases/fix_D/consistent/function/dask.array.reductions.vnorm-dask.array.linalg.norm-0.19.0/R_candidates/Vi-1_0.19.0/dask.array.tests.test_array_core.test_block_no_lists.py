@pytest.mark.skipif(LooseVersion(np.__version__) < '1.13.0',
                    reason="NumPy doesn't support `block` yet")
def test_block_no_lists():
    assert_eq(da.block(1),         np.block(1))
    assert_eq(da.block(np.eye(3)), np.block(np.eye(3)))
