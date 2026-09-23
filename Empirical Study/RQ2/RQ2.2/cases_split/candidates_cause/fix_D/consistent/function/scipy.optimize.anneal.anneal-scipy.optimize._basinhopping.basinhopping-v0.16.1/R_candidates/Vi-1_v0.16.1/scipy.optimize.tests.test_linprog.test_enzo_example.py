def test_enzo_example():
    # http://projects.scipy.org/scipy/attachment/ticket/1252/lp2.py
    #
    # Translated from Octave code at:
    # http://www.ecs.shimane-u.ac.jp/~kyoshida/lpeng.htm
    # and placed under MIT licence by Enzo Michelangeli
    # with permission explicitly granted by the original author,
    # Prof. Kazunobu Yoshida  
    c = [4, 8, 3, 0, 0, 0]
    A_eq = [
            [2, 5, 3, -1, 0, 0],
            [3, 2.5, 8, 0, -1, 0],
            [8, 10, 4, 0, 0, -1]]
    b_eq = [185, 155, 600]
    res = linprog(c=c, A_eq=A_eq, b_eq=b_eq)
    _assert_success(res, desired_fun=317.5,
                    desired_x=[66.25, 0, 17.5, 0, 183.75, 0])
