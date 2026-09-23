@pytest.mark.parametrize('chunks,index,expected', [
    (
        (5, 5, 5),
        np.arange(5, 15) % 10,
        [(1, np.arange(5)),
         (0, np.arange(5))]
    ),
    (
        (5, 5, 5, 5),
        np.arange(20) // 2,
        [(0, np.arange(10) // 2),
         (1, np.arange(10) // 2)]
    ),
    (
        (10, 10),
        [15, 2, 3, 15],
        [(1, [5]),
         (0, [2, 3]),
         (1, [5])]
    ),
])
def test_slicing_plan(chunks, index, expected):
    plan = slicing_plan(chunks, index)
    assert len(plan) == len(expected)
    for (i, x), (j, y) in zip(plan, expected):
        assert i == j
        assert len(x) == len(y)
        assert (x == y).all()
