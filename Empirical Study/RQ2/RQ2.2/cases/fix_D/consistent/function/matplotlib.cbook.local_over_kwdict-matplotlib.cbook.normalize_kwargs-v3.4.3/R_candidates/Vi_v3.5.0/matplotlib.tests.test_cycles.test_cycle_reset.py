def test_cycle_reset():
    fig, ax = plt.subplots()

    # Can't really test a reset because only a cycle object is stored
    # but we can test the first item of the cycle.
    prop = next(ax._get_lines.prop_cycler)
    ax.set_prop_cycle(linewidth=[10, 9, 4])
    assert prop != next(ax._get_lines.prop_cycler)
    ax.set_prop_cycle(None)
    got = next(ax._get_lines.prop_cycler)
    assert prop == got
