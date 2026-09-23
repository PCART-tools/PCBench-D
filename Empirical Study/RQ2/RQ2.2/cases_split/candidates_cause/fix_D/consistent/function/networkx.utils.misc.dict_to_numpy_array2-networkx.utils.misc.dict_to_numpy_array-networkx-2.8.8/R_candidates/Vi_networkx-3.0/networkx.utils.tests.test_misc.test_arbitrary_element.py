@pytest.mark.parametrize(
    ("iterable_type", "expected"), ((list, 1), (tuple, 1), (str, "["), (set, 1))
)
def test_arbitrary_element(iterable_type, expected):
    iterable = iterable_type([1, 2, 3])
    assert arbitrary_element(iterable) == expected
