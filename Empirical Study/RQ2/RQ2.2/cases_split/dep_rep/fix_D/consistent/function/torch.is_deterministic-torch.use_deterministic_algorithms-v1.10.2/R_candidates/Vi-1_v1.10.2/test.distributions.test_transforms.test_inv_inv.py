@pytest.mark.parametrize('transform', ALL_TRANSFORMS, ids=transform_id)
def test_inv_inv(transform, ids=transform_id):
    assert transform.inv.inv is transform
