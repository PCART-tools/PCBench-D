    def test_scatter_singular_plural_arguments(self):

        with pytest.raises(TypeError,
                           match="Got both 'linewidth' and 'linewidths',\
 which are aliases of one another"):
            plt.scatter([1, 2, 3], [1, 2, 3], linewidths=[0.5, 0.4, 0.3], linewidth=0.2)

        with pytest.raises(TypeError,
                           match="Got both 'edgecolor' and 'edgecolors',\
 which are aliases of one another"):
            plt.scatter([1, 2, 3], [1, 2, 3],
                        edgecolors=["#ffffff", "#000000", "#f0f0f0"],
                          edgecolor="#ffffff")

        with pytest.raises(TypeError,
                           match="Got both 'facecolors' and 'facecolor',\
 which are aliases of one another"):
            plt.scatter([1, 2, 3], [1, 2, 3],
                        facecolors=["#ffffff", "#000000", "#f0f0f0"],
                            facecolor="#ffffff")
