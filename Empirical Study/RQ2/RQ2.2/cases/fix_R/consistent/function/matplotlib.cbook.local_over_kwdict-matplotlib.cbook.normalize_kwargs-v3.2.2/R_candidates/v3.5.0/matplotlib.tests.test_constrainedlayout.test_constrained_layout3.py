@image_comparison(['constrained_layout3.png'])
def test_constrained_layout3():
    """Test constrained_layout for colorbars with subplots"""

    fig, axs = plt.subplots(2, 2, constrained_layout=True)
    for nn, ax in enumerate(axs.flat):
        pcm = example_pcolor(ax, fontsize=24)
        if nn == 3:
            pad = 0.08
        else:
            pad = 0.02  # default
        fig.colorbar(pcm, ax=ax, pad=pad)
