@pytest.mark.slow
@pytest.mark.parametrize('size', [10, 20, 30, 50])
def test_lu_2(size):
    np.random.seed(10)
    A = np.random.randint(0, 10, (size, size))

    dA = da.from_array(A, chunks=(5, 5))
    dp, dl, du = da.linalg.lu(dA)
    _check_lu_result(dp, dl, du, A)
