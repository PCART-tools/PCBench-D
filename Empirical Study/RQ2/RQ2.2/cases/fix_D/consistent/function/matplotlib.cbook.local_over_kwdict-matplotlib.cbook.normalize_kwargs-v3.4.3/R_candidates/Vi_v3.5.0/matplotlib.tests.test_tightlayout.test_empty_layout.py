def test_empty_layout():
    """Test that tight layout doesn't cause an error when there are no axes."""
    fig = plt.gcf()
    fig.tight_layout()
