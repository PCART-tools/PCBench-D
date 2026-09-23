def test_chi2_contingency_R():
    # Some test cases that were computed independently, using R.

    Rcode = \
    """
    # Data vector.
    data <- c(
      12, 34, 23,     4,  47,  11,
      35, 31, 11,    34,  10,  18,
      12, 32,  9,    18,  13,  19,
      12, 12, 14,     9,  33,  25
      )

    # Create factor tags:r=rows, c=columns, t=tiers
    r <- factor(gl(4, 2*3, 2*3*4, labels=c("r1", "r2", "r3", "r4")))
    c <- factor(gl(3, 1,   2*3*4, labels=c("c1", "c2", "c3")))
    t <- factor(gl(2, 3,   2*3*4, labels=c("t1", "t2")))

    # 3-way Chi squared test of independence
    s = summary(xtabs(data~r+c+t))
    print(s)
    """
    Routput = \
    """
    Call: xtabs(formula = data ~ r + c + t)
    Number of cases in table: 478
    Number of factors: 3
    Test for independence of all factors:
            Chisq = 102.17, df = 17, p-value = 3.514e-14
    """
    obs = np.array(
        [[[12, 34, 23],
          [35, 31, 11],
          [12, 32, 9],
          [12, 12, 14]],
         [[4, 47, 11],
          [34, 10, 18],
          [18, 13, 19],
          [9, 33, 25]]])
    chi2, p, dof, expected = chi2_contingency(obs)
    assert_approx_equal(chi2, 102.17, significant=5)
    assert_approx_equal(p, 3.514e-14, significant=4)
    assert_equal(dof, 17)

    Rcode = \
    """
    # Data vector.
    data <- c(
        #
        12, 17,
        11, 16,
        #
        11, 12,
        15, 16,
        #
        23, 15,
        30, 22,
        #
        14, 17,
        15, 16
        )

    # Create factor tags:r=rows, c=columns, d=depths(?), t=tiers
    r <- factor(gl(2, 2,  2*2*2*2, labels=c("r1", "r2")))
    c <- factor(gl(2, 1,  2*2*2*2, labels=c("c1", "c2")))
    d <- factor(gl(2, 4,  2*2*2*2, labels=c("d1", "d2")))
    t <- factor(gl(2, 8,  2*2*2*2, labels=c("t1", "t2")))

    # 4-way Chi squared test of independence
    s = summary(xtabs(data~r+c+d+t))
    print(s)
    """
    Routput = \
    """
    Call: xtabs(formula = data ~ r + c + d + t)
    Number of cases in table: 262
    Number of factors: 4
    Test for independence of all factors:
            Chisq = 8.758, df = 11, p-value = 0.6442
    """
    obs = np.array(
        [[[[12, 17],
           [11, 16]],
          [[11, 12],
           [15, 16]]],
         [[[23, 15],
           [30, 22]],
          [[14, 17],
           [15, 16]]]])
    chi2, p, dof, expected = chi2_contingency(obs)
    assert_approx_equal(chi2, 8.758, significant=4)
    assert_approx_equal(p, 0.6442, significant=4)
    assert_equal(dof, 11)
