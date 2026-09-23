@image_comparison(['constrained_layout15.png'])
def test_constrained_layout15():
    """Test that rcparams work."""
    rcParams['figure.constrained_layout.use'] = True
    fig, axs = plt.subplots(2, 2)
    for ax in axs.flat:
        example_plot(ax, fontsize=12)
