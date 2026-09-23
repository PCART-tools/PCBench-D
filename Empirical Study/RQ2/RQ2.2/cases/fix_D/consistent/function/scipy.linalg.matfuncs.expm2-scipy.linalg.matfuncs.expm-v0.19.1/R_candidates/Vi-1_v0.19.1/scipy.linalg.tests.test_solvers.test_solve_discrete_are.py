def test_solve_discrete_are():

    cases = [
        # Darex examples taken from (with default parameters):
        # [1] P.BENNER, A.J. LAUB, V. MEHRMANN: 'A Collection of Benchmark
        #     Examples for the Numerical Solution of Algebraic Riccati
        #     Equations II: Discrete-Time Case', Tech. Report SPC 95_23,
        #     Fak. f. Mathematik, TU Chemnitz-Zwickau (Germany), 1995.
        # [2] T. GUDMUNDSSON, C. KENNEY, A.J. LAUB: 'Scaling of the
        #     Discrete-Time Algebraic Riccati Equation to Enhance Stability
        #     of the Schur Solution Method', IEEE Trans.Aut.Cont., vol.37(4)
        #
        # The format of the data is (a, b, q, r, knownfailure), where
        # knownfailure is None if the test passes or a string
        # indicating the reason for failure.
        #
        # TEST CASE 0 : Complex a; real b, q, r
        (np.array([[2, 1-2j], [0, -3j]]),
         np.array([[0], [1]]),
         np.array([[1, 0], [0, 2]]),
         np.array([[1]]),
         None),
        # TEST CASE 1 :Real a, q, r; complex b
        (np.array([[2, 1], [0, -1]]),
         np.array([[-2j], [1j]]),
         np.array([[1, 0], [0, 2]]),
         np.array([[1]]),
         None),
        # TEST CASE 2 : Real a, b; complex q, r
        (np.array([[3, 1], [0, -1]]),
         np.array([[1, 2], [1, 3]]),
         np.array([[1, 1+1j], [1-1j, 2]]),
         np.array([[2, -2j], [2j, 3]]),
         None),
        # TEST CASE 3 : User-reported gh-2251 (Trac #1732)
        (np.array([[0.63399379, 0.54906824, 0.76253406],
                   [0.5404729, 0.53745766, 0.08731853],
                   [0.27524045, 0.84922129, 0.4681622]]),
         np.array([[0.96861695], [0.05532739], [0.78934047]]),
         np.eye(3),
         np.eye(1),
         None),
        # TEST CASE 4 : darex #1
        (np.array([[4, 3], [-4.5, -3.5]]),
         np.array([[1], [-1]]),
         np.array([[9, 6], [6, 4]]),
         np.array([[1]]),
         None),
        # TEST CASE 5 : darex #2
        (np.array([[0.9512, 0], [0, 0.9048]]),
         np.array([[4.877, 4.877], [-1.1895, 3.569]]),
         np.array([[0.005, 0], [0, 0.02]]),
         np.array([[1/3, 0], [0, 3]]),
         None),
        # TEST CASE 6 : darex #3
        (np.array([[2, -1], [1, 0]]),
         np.array([[1], [0]]),
         np.array([[0, 0], [0, 1]]),
         np.array([[0]]),
         None),
        # TEST CASE 7 : darex #4 (skipped the gen. Ric. term S)
        (np.array([[0, 1], [0, -1]]),
         np.array([[1, 0], [2, 1]]),
         np.array([[-4, -4], [-4, 7]]) * (1/11),
         np.array([[9, 3], [3, 1]]),
         None),
        # TEST CASE 8 : darex #5
        (np.array([[0, 1], [0, 0]]),
         np.array([[0], [1]]),
         np.array([[1, 2], [2, 4]]),
         np.array([[1]]),
         None),
        # TEST CASE 9 : darex #6
        (np.array([[0.998, 0.067, 0, 0],
                   [-.067, 0.998, 0, 0],
                   [0, 0, 0.998, 0.153],
                   [0, 0, -.153, 0.998]]),
         np.array([[0.0033, 0.0200],
                   [0.1000, -.0007],
                   [0.0400, 0.0073],
                   [-.0028, 0.1000]]),
         np.array([[1.87, 0, 0, -0.244],
                   [0, 0.744, 0.205, 0],
                   [0, 0.205, 0.589, 0],
                   [-0.244, 0, 0, 1.048]]),
         np.eye(2),
         None),
        # TEST CASE 10 : darex #7
        (np.array([[0.984750, -.079903, 0.0009054, -.0010765],
                   [0.041588, 0.998990, -.0358550, 0.0126840],
                   [-.546620, 0.044916, -.3299100, 0.1931800],
                   [2.662400, -.100450, -.9245500, -.2632500]]),
         np.array([[0.0037112, 0.0007361],
                   [-.0870510, 9.3411e-6],
                   [-1.198440, -4.1378e-4],
                   [-3.192700, 9.2535e-4]]),
         np.eye(4)*1e-2,
         np.eye(2),
         None),
        # TEST CASE 11 : darex #8
        (np.array([[-0.6000000, -2.2000000, -3.6000000, -5.4000180],
                   [1.0000000, 0.6000000, 0.8000000, 3.3999820],
                   [0.0000000, 1.0000000, 1.8000000, 3.7999820],
                   [0.0000000, 0.0000000, 0.0000000, -0.9999820]]),
         np.array([[1.0, -1.0, -1.0, -1.0],
                   [0.0, 1.0, -1.0, -1.0],
                   [0.0, 0.0, 1.0, -1.0],
                   [0.0, 0.0, 0.0, 1.0]]),
         np.array([[2, 1, 3, 6],
                   [1, 2, 2, 5],
                   [3, 2, 6, 11],
                   [6, 5, 11, 22]]),
         np.eye(4),
         None),
        # TEST CASE 12 : darex #9
        (np.array([[95.4070, 1.9643, 0.3597, 0.0673, 0.0190],
                   [40.8490, 41.3170, 16.0840, 4.4679, 1.1971],
                   [12.2170, 26.3260, 36.1490, 15.9300, 12.3830],
                   [4.1118, 12.8580, 27.2090, 21.4420, 40.9760],
                   [0.1305, 0.5808, 1.8750, 3.6162, 94.2800]]) * 0.01,
         np.array([[0.0434, -0.0122],
                   [2.6606, -1.0453],
                   [3.7530, -5.5100],
                   [3.6076, -6.6000],
                   [0.4617, -0.9148]]) * 0.01,
         np.eye(5),
         np.eye(2),
         None),
        # TEST CASE 13 : darex #10
        (np.kron(np.eye(2), np.diag([1, 1], k=1)),
         np.kron(np.eye(2), np.array([[0], [0], [1]])),
         np.array([[1, 1, 0, 0, 0, 0],
                   [1, 1, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, -1, 0],
                   [0, 0, 0, -1, 1, 0],
                   [0, 0, 0, 0, 0, 0]]),
         np.array([[3, 0], [0, 1]]),
         None),
        # TEST CASE 14 : darex #11
        (0.001 * np.array(
         [[870.1, 135.0, 11.59, .5014, -37.22, .3484, 0, 4.242, 7.249],
          [76.55, 897.4, 12.72, 0.5504, -40.16, .3743, 0, 4.53, 7.499],
          [-127.2, 357.5, 817, 1.455, -102.8, .987, 0, 11.85, 18.72],
          [-363.5, 633.9, 74.91, 796.6, -273.5, 2.653, 0, 31.72, 48.82],
          [-960, 1645.9, -128.9, -5.597, 71.42, 7.108, 0, 84.52, 125.9],
          [-664.4, 112.96, -88.89, -3.854, 84.47, 13.6, 0, 144.3, 101.6],
          [-410.2, 693, -54.71, -2.371, 66.49, 12.49, .1063, 99.97, 69.67],
          [-179.9, 301.7, -23.93, -1.035, 60.59, 22.16, 0, 213.9, 35.54],
          [-345.1, 580.4, -45.96, -1.989, 105.6, 19.86, 0, 219.1, 215.2]]),
         np.array([[4.7600, -0.5701, -83.6800],
                   [0.8790, -4.7730, -2.7300],
                   [1.4820, -13.1200, 8.8760],
                   [3.8920, -35.1300, 24.8000],
                   [10.3400, -92.7500, 66.8000],
                   [7.2030, -61.5900, 38.3400],
                   [4.4540, -36.8300, 20.2900],
                   [1.9710, -15.5400, 6.9370],
                   [3.7730, -30.2800, 14.6900]]) * 0.001,
         np.diag([50, 0, 0, 0, 50, 0, 0, 0, 0]),
         np.eye(3),
         None),
        # TEST CASE 15 : darex #12 - numerically least accurate example
        (np.array([[0, 1e6], [0, 0]]),
         np.array([[0], [1]]),
         np.eye(2),
         np.array([[1]]),
         None),
        # TEST CASE 16 : darex #13
        (np.array([[16, 10, -2],
                  [10, 13, -8],
                  [-2, -8, 7]]) * (1/9),
         np.eye(3),
         1e6 * np.eye(3),
         1e6 * np.eye(3),
         None),
        # TEST CASE 17 : darex #14
        (np.array([[1 - 1/1e8, 0, 0, 0],
                  [1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0]]),
         np.array([[1e-08], [0], [0], [0]]),
         np.diag([0, 0, 0, 1]),
         np.array([[0.25]]),
         None),
        # TEST CASE 18 : darex #15
        (np.eye(100, k=1),
         np.flipud(np.eye(100, 1)),
         np.eye(100),
         np.array([[1]]),
         None)
        ]

    # Makes the minimum precision requirements customized to the test.
    # Here numbers represent the number of decimals that agrees with zero
    # matrix when the solution x is plugged in to the equation.
    #
    # res = array([[8e-3,1e-16],[1e-16,1e-20]]) --> min_decimal[k] = 2
    #
    # If the test is failing use "None" for that entry.
    #
    min_decimal = (12, 14, 13, 14, 13, 16, 18, 14, 15, 13,
                   14, 13, 13, 14, 12, 2, 5, 6, 10)

    def _test_factory(case, dec):
        """Checks if X = A'XA-(A'XB)(R+B'XB)^-1(B'XA)+Q) is true"""
        a, b, q, r, knownfailure = case
        if knownfailure:
            raise KnownFailureTest(knownfailure)

        x = solve_discrete_are(a, b, q, r)
        res = a.conj().T.dot(x.dot(a)) - x + q
        res -= a.conj().T.dot(x.dot(b)).dot(
                    solve(r+b.conj().T.dot(x.dot(b)), b.conj().T).dot(x.dot(a))
                    )
        assert_array_almost_equal(res, np.zeros_like(res), decimal=dec)

    for ind, case in enumerate(cases):
        yield _test_factory, case, min_decimal[ind]
