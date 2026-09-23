def test_shared():
    rdim = (4, 4, 2)
    share = {
            'all': np.ones(rdim[:2], dtype=bool),
            'none': np.zeros(rdim[:2], dtype=bool),
            'row': np.array([
                [False, True, False, False],
                [True, False, False, False],
                [False, False, False, True],
                [False, False, True, False]]),
            'col': np.array([
                [False, False, True, False],
                [False, False, False, True],
                [True, False, False, False],
                [False, True, False, False]]),
            }
    visible = {
            'x': {
                'all': [False, False, True, True],
                'col': [False, False, True, True],
                'row': [True] * 4,
                'none': [True] * 4,
                False: [True] * 4,
                True: [False, False, True, True],
                },
            'y': {
                'all': [True, False, True, False],
                'col': [True] * 4,
                'row': [True, False, True, False],
                'none': [True] * 4,
                False: [True] * 4,
                True: [True, False, True, False],
                },
            }
    share[False] = share['none']
    share[True] = share['all']

    # test default
    f, ((a1, a2), (a3, a4)) = plt.subplots(2, 2)
    axs = [a1, a2, a3, a4]
    check_shared(axs, share['none'], share['none'])
    plt.close(f)

    # test all option combinations
    ops = [False, True, 'all', 'none', 'row', 'col']
    for xo in ops:
        for yo in ops:
            f, ((a1, a2), (a3, a4)) = plt.subplots(2, 2, sharex=xo, sharey=yo)
            axs = [a1, a2, a3, a4]
            check_shared(axs, share[xo], share[yo])
            check_visible(axs, visible['x'][xo], visible['y'][yo])
            plt.close(f)

    # test label_outer
    f, ((a1, a2), (a3, a4)) = plt.subplots(2, 2, sharex=True, sharey=True)
    axs = [a1, a2, a3, a4]
    for ax in axs:
        ax.label_outer()
    check_visible(axs, [False, False, True, True], [True, False, True, False])
