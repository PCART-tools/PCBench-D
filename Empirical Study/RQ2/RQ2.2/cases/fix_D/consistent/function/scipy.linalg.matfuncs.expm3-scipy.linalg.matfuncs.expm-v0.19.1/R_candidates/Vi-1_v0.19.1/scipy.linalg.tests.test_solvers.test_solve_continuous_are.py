def test_solve_continuous_are():
    mat6 = np.load(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                'data', 'carex_6_data.npz'))
    mat15 = np.load(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'data', 'carex_15_data.npz'))
    mat18 = np.load(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'data', 'carex_18_data.npz'))
    mat19 = np.load(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'data', 'carex_19_data.npz'))
    mat20 = np.load(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'data', 'carex_20_data.npz'))
    cases = [
        # Carex examples taken from (with default parameters):
        # [1] P.BENNER, A.J. LAUB, V. MEHRMANN: 'A Collection of Benchmark
        #     Examples for the Numerical Solution of Algebraic Riccati
        #     Equations II: Continuous-Time Case', Tech. Report SPC 95_23,
        #     Fak. f. Mathematik, TU Chemnitz-Zwickau (Germany), 1995.
        #
        # The format of the data is (a, b, q, r, knownfailure), where
        # knownfailure is None if the test passes or a string
        # indicating the reason for failure.
        #
        # Test Case 0: carex #1
        (np.diag([1.], 1),
         np.array([[0], [1]]),
         block_diag(1., 2.),
         1,
         None),
        # Test Case 1: carex #2
        (np.array([[4, 3], [-4.5, -3.5]]),
         np.array([[1], [-1]]),
         np.array([[9, 6], [6, 4.]]),
         1,
         None),
        # Test Case 2: carex #3
        (np.array([[0, 1, 0, 0],
                   [0, -1.89, 0.39, -5.53],
                   [0, -0.034, -2.98, 2.43],
                   [0.034, -0.0011, -0.99, -0.21]]),
         np.array([[0, 0], [0.36, -1.6], [-0.95, -0.032], [0.03, 0]]),
         np.array([[2.313, 2.727, 0.688, 0.023],
                   [2.727, 4.271, 1.148, 0.323],
                   [0.688, 1.148, 0.313, 0.102],
                   [0.023, 0.323, 0.102, 0.083]]),
         np.eye(2),
         None),
        # Test Case 3: carex #4
        (np.array([[-0.991, 0.529, 0, 0, 0, 0, 0, 0],
                   [0.522, -1.051, 0.596, 0, 0, 0, 0, 0],
                   [0, 0.522, -1.118, 0.596, 0, 0, 0, 0],
                   [0, 0, 0.522, -1.548, 0.718, 0, 0, 0],
                   [0, 0, 0, 0.922, -1.64, 0.799, 0, 0],
                   [0, 0, 0, 0, 0.922, -1.721, 0.901, 0],
                   [0, 0, 0, 0, 0, 0.922, -1.823, 1.021],
                   [0, 0, 0, 0, 0, 0, 0.922, -1.943]]),
         np.array([[3.84, 4.00, 37.60, 3.08, 2.36, 2.88, 3.08, 3.00],
                   [-2.88, -3.04, -2.80, -2.32, -3.32, -3.82, -4.12, -3.96]]
                  ).T * 0.001,
         np.array([[1.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.1],
                   [0.0, 1.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0],
                   [0.0, 0.0, 1.0, 0.0, 0.0, 0.5, 0.0, 0.0],
                   [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                   [0.5, 0.1, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0],
                   [0.0, 0.0, 0.5, 0.0, 0.0, 0.1, 0.0, 0.0],
                   [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0],
                   [0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1]]),
         np.eye(2),
         None),
        # Test Case 4: carex #5
        (np.array(
          [[-4.019, 5.120, 0., 0., -2.082, 0., 0., 0., 0.870],
           [-0.346, 0.986, 0., 0., -2.340, 0., 0., 0., 0.970],
           [-7.909, 15.407, -4.069, 0., -6.450, 0., 0., 0., 2.680],
           [-21.816, 35.606, -0.339, -3.870, -17.800, 0., 0., 0., 7.390],
           [-60.196, 98.188, -7.907, 0.340, -53.008, 0., 0., 0., 20.400],
           [0, 0, 0, 0, 94.000, -147.200, 0., 53.200, 0.],
           [0, 0, 0, 0, 0, 94.000, -147.200, 0, 0],
           [0, 0, 0, 0, 0, 12.800, 0.000, -31.600, 0],
           [0, 0, 0, 0, 12.800, 0.000, 0.000, 18.800, -31.600]]),
         np.array([[0.010, -0.011, -0.151],
                   [0.003, -0.021, 0.000],
                   [0.009, -0.059, 0.000],
                   [0.024, -0.162, 0.000],
                   [0.068, -0.445, 0.000],
                   [0.000, 0.000, 0.000],
                   [0.000, 0.000, 0.000],
                   [0.000, 0.000, 0.000],
                   [0.000, 0.000, 0.000]]),
         np.eye(9),
         np.eye(3),
         None),
        # Test Case 5: carex #6
        (mat6['A'], mat6['B'], mat6['Q'], mat6['R'], None),
        # Test Case 6: carex #7
        (np.array([[1, 0], [0, -2.]]),
         np.array([[1e-6], [0]]),
         np.ones((2, 2)),
         1.,
         'Bad residual accuracy'),
        # Test Case 7: carex #8
        (block_diag(-0.1, -0.02),
         np.array([[0.100, 0.000], [0.001, 0.010]]),
         np.array([[100, 1000], [1000, 10000]]),
         np.ones((2, 2)) + block_diag(1e-6, 0),
         None),
        # Test Case 8: carex #9
        (np.array([[0, 1e6], [0, 0]]),
         np.array([[0], [1.]]),
         np.eye(2),
         1.,
         None),
        # Test Case 9: carex #10
        (np.array([[1.0000001, 1], [1., 1.0000001]]),
         np.eye(2),
         np.eye(2),
         np.eye(2),
         None),
        # Test Case 10: carex #11
        (np.array([[3, 1.], [4, 2]]),
         np.array([[1], [1]]),
         np.array([[-11, -5], [-5, -2.]]),
         1.,
         None),
        # Test Case 11: carex #12
        (np.array([[7000000., 2000000., -0.],
                   [2000000., 6000000., -2000000.],
                   [0., -2000000., 5000000.]]) / 3,
         np.eye(3),
         np.array([[1., -2., -2.], [-2., 1., -2.], [-2., -2., 1.]]).dot(
                np.diag([1e-6, 1, 1e6])).dot(
            np.array([[1., -2., -2.], [-2., 1., -2.], [-2., -2., 1.]])) / 9,
         np.eye(3) * 1e6,
         'Bad Residual Accuracy'),
        # Test Case 12: carex #13
        (np.array([[0, 0.4, 0, 0],
                   [0, 0, 0.345, 0],
                   [0, -0.524e6, -0.465e6, 0.262e6],
                   [0, 0, 0, -1e6]]),
         np.array([[0, 0, 0, 1e6]]).T,
         np.diag([1, 0, 1, 0]),
         1.,
         None),
        # Test Case 13: carex #14
        (np.array([[-1e-6, 1, 0, 0],
                   [-1, -1e-6, 0, 0],
                   [0, 0, 1e-6, 1],
                   [0, 0, -1, 1e-6]]),
         np.ones((4, 1)),
         np.ones((4, 4)),
         1.,
         None),
        # Test Case 14: carex #15
        (mat15['A'], mat15['B'], mat15['Q'], mat15['R'], None),
        # Test Case 15: carex #16
        (np.eye(64, 64, k=-1) + np.eye(64, 64)*(-2.) + np.rot90(
                 block_diag(1, np.zeros((62, 62)), 1)) + np.eye(64, 64, k=1),
         np.eye(64),
         np.eye(64),
         np.eye(64),
         None),
        # Test Case 16: carex #17
        (np.diag(np.ones((20, )), 1),
         np.flipud(np.eye(21, 1)),
         np.eye(21, 1) * np.eye(21, 1).T,
         1,
         'Bad Residual Accuracy'),
        # Test Case 17: carex #18
        (mat18['A'], mat18['B'], mat18['Q'], mat18['R'], None),
        # Test Case 18: carex #19
        (mat19['A'], mat19['B'], mat19['Q'], mat19['R'],
         'Bad Residual Accuracy'),
        # Test Case 19: carex #20
        (mat20['A'], mat20['B'], mat20['Q'], mat20['R'],
         'Bad Residual Accuracy')
        ]
    # Makes the minimum precision requirements customized to the test.
    # Here numbers represent the number of decimals that agrees with zero
    # matrix when the solution x is plugged in to the equation.
    #
    # res = array([[8e-3,1e-16],[1e-16,1e-20]]) --> min_decimal[k] = 2
    #
    # If the test is failing use "None" for that entry.
    #
    min_decimal = (14, 12, 13, 14, 11, 6, None, 5, 7, 14, 14,
                   None, 9, 14, 13, 14, None, 12, None, None)

    def _test_factory(case, dec):
        """Checks if 0 = XA + A'X - XB(R)^{-1} B'X + Q is true"""
        a, b, q, r, knownfailure = case
        if knownfailure:
            raise KnownFailureTest(knownfailure)

        x = solve_continuous_are(a, b, q, r)
        res = x.dot(a) + a.conj().T.dot(x) + q
        out_fact = x.dot(b)
        res -= out_fact.dot(solve(np.atleast_2d(r), out_fact.conj().T))
        assert_array_almost_equal(res, np.zeros_like(res), decimal=dec)

    for ind, case in enumerate(cases):
        yield _test_factory, case, min_decimal[ind]
