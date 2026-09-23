@pytest.mark.parametrize("boundary", [
    None,
    "reflect",
    "periodic",
    "nearest",
    "none",
    0
])
def test_map_overlap_no_depth(boundary):
    x = da.arange(10, chunks=5)

    y = x.map_overlap(lambda i: i, depth=0, boundary=boundary, dtype=x.dtype)
    assert_eq(y, x)
