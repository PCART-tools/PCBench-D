@image_comparison(['constrained_layout4.png'])
def test_constrained_layout4():
    """Test constrained_layout for a single colorbar with subplots"""
    # Remove this line when this test image is regenerated.
    plt.rcParams['pcolormesh.snap'] = False

    fig, axs = plt.subplots(2, 2, constrained_layout=True)
    for ax in axs.flat:
        pcm = example_pcolor(ax, fontsize=24)
    fig.colorbar(pcm, ax=axs, pad=0.01, shrink=0.6)
