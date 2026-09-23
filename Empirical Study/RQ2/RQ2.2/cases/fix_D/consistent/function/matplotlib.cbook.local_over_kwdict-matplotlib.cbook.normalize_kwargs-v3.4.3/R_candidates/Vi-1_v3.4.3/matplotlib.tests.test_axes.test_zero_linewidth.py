def test_zero_linewidth():
    # Check that setting a zero linewidth doesn't error
    plt.plot([0, 1], [0, 1], ls='--', lw=0)
