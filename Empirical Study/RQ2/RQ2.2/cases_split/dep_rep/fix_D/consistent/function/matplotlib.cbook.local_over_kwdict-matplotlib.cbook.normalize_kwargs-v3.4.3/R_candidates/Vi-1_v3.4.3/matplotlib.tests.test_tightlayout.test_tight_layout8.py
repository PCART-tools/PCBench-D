@image_comparison(['tight_layout8'])
def test_tight_layout8():
    """Test automatic use of tight_layout."""
    fig = plt.figure()
    fig.set_tight_layout({'pad': .1})
    ax = fig.add_subplot()
    example_plot(ax, fontsize=24)
