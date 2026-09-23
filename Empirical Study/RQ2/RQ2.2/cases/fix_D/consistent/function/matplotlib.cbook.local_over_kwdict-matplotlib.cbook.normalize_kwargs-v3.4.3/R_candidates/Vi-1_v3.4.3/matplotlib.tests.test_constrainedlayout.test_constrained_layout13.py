@image_comparison(['constrained_layout13.png'], tol=2.e-2)
def test_constrained_layout13():
    """Test that padding works."""
    # Remove this line when this test image is regenerated.
    plt.rcParams['pcolormesh.snap'] = False

    fig, axs = plt.subplots(2, 2, constrained_layout=True)
    for ax in axs.flat:
        pcm = example_pcolor(ax, fontsize=12)
        fig.colorbar(pcm, ax=ax, shrink=0.6, aspect=20., pad=0.02)
    fig.set_constrained_layout_pads(w_pad=24./72., h_pad=24./72.)
