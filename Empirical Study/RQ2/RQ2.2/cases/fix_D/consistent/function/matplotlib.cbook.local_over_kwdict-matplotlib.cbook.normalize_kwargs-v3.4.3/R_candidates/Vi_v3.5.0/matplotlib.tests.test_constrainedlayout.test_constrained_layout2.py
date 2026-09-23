@image_comparison(['constrained_layout2.png'])
def test_constrained_layout2():
    """Test constrained_layout for 2x2 subplots"""
    fig, axs = plt.subplots(2, 2, constrained_layout=True)
    for ax in axs.flat:
        example_plot(ax, fontsize=24)
