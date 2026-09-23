@needs_usetex
def test_failing_latex():
    """Test failing latex subprocess call"""
    mpl.rcParams['text.usetex'] = True
    # This fails with "Double subscript"
    plt.xlabel("$22_2_2$")
    with pytest.raises(RuntimeError):
        plt.savefig(io.BytesIO(), format="ps")
