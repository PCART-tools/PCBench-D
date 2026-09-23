    def test_scatter_norm_vminvmax(self):
        """Parameters vmin, vmax should error if norm is given."""
        x = [1, 2, 3]
        ax = plt.axes()
        with pytest.raises(ValueError,
                           match="Passing a Normalize instance simultaneously "
                                 "with vmin/vmax is not supported."):
            ax.scatter(x, x, c=x, norm=mcolors.Normalize(-10, 10),
                       vmin=0, vmax=5)
