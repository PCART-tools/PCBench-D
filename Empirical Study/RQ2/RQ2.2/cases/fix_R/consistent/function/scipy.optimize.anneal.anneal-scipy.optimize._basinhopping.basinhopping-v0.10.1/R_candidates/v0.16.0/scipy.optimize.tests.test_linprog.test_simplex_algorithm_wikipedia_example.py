def test_simplex_algorithm_wikipedia_example():
    # http://en.wikipedia.org/wiki/Simplex_algorithm#Example
    Z = [-2, -3, -4]
    A_ub = [
            [3, 2, 1],
            [2, 5, 3]]
    b_ub = [10, 15]
    res = linprog(c=Z, A_ub=A_ub, b_ub=b_ub)
    _assert_success(res, desired_fun=-20)
