def test_power_divergence_against_cressie_read_data():
    # Test stats.power_divergence against tables 4 and 5 from
    # Cressie and Read, "Multimonial Goodness-of-Fit Tests",
    # J. R. Statist. Soc. B (1984), Vol 46, No. 3, pp. 440-464.
    # This tests the calculation for several values of lambda.

    # `table4` holds just the second and third columns from Table 4.
    table4 = np.array([
        # observed, expected,
        15, 15.171,
        11, 13.952,
        14, 12.831,
        17, 11.800,
        5, 10.852,
        11, 9.9796,
        10, 9.1777,
        4, 8.4402,
        8, 7.7620,
        10, 7.1383,
        7, 6.5647,
        9, 6.0371,
        11, 5.5520,
        3, 5.1059,
        6, 4.6956,
        1, 4.3183,
        1, 3.9713,
        4, 3.6522,
        ]).reshape(-1, 2)
    table5 = np.array([
        # lambda, statistic
        -10.0, 72.2e3,
        -5.0, 28.9e1,
        -3.0, 65.6,
        -2.0, 40.6,
        -1.5, 34.0,
        -1.0, 29.5,
        -0.5, 26.5,
        0.0, 24.6,
        0.5, 23.4,
        0.67, 23.1,
        1.0, 22.7,
        1.5, 22.6,
        2.0, 22.9,
        3.0, 24.8,
        5.0, 35.5,
        10.0, 21.4e1,
        ]).reshape(-1, 2)

    for lambda_, expected_stat in table5:
        stat, p = stats.power_divergence(table4[:,0], table4[:,1],
                                         lambda_=lambda_)
        assert_allclose(stat, expected_stat, rtol=5e-3)
