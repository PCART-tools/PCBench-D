@check_figures_equal(extensions=('png',))
def test_markevery(fig_test, fig_ref):
    np.random.seed(42)
    t = np.linspace(0, 3, 14)
    y = np.random.rand(len(t))

    casesA = [None, 4, (2, 5), [1, 5, 11],
              [0, -1], slice(5, 10, 2), 0.3, (0.3, 0.4),
              np.arange(len(t))[y > 0.5]]
    casesB = ["11111111111111", "10001000100010", "00100001000010",
              "01000100000100", "10000000000001", "00000101010000",
              "11011011011110", "01010011011101", "01110001110110"]

    axsA = fig_ref.subplots(3, 3)
    axsB = fig_test.subplots(3, 3)

    for ax, case in zip(axsA.flat, casesA):
        ax.plot(t, y, "-gD", markevery=case)

    for ax, case in zip(axsB.flat, casesB):
        me = np.array(list(case)).astype(int).astype(bool)
        ax.plot(t, y, "-gD", markevery=me)
