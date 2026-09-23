    @pytest.mark.xfail(reason="Test for clabel not written yet")
    @mpl.style.context("default")
    def test_clabel(self):
        fig, ax = plt.subplots()
        ax.clabel(...)
