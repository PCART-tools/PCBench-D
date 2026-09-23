    @pytest.mark.xfail(reason="Test for streamplot not written yet")
    @mpl.style.context("default")
    def test_streamplot(self):
        fig, ax = plt.subplots()
        ax.streamplot(...)
