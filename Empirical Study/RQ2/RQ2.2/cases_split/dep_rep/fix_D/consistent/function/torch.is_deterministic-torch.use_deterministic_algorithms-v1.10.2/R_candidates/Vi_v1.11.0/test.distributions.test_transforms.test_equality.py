@pytest.mark.parametrize('x', TRANSFORMS_CACHE_INACTIVE, ids=transform_id)
@pytest.mark.parametrize('y', TRANSFORMS_CACHE_INACTIVE, ids=transform_id)
def test_equality(x, y):
    if x is y:
        assert x == y
    else:
        assert x != y
    assert identity_transform == identity_transform.inv
