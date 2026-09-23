@pytest.mark.thread_unsafe
def test_trapz_deprecation():
    with pytest.deprecated_call(match="`quadrature='trapz'`"):
        quad_vec(lambda x: x, 0, 1, quadrature="trapz")
