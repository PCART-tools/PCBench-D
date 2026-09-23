@pytest.mark.parametrize('size', [50, 100, 200])
def test_lu_3(size):
    np.random.seed(10)
    A = np.random.random_integers(0, 10, (size, size))

    dA = da.from_array(A, chunks=(25, 25))
    dp, dl, du = da.linalg.lu(dA)
    _check_lu_result(dp, dl, du, A)
