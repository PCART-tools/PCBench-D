@image_comparison(['constrained_layout1.png'])
def test_constrained_layout1():
    """Test constrained_layout for a single subplot"""
    fig = plt.figure(constrained_layout=True)
    ax = fig.add_subplot()
    example_plot(ax, fontsize=24)
