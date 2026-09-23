    def test_update_plot_heterogenous_plotter(self):
        ax = plt.figure().subplots()
        ax.scatter(['a', 'b'], ['e', 'g'])
        ax.plot(['a', 'b', 'd'], ['f', 'a', 'b'])
        ax.bar(['b', 'c', 'd'], ['g', 'e', 'd'])
        axis_test(ax.xaxis, ['a', 'b', 'd', 'c'])
        axis_test(ax.yaxis, ['e', 'g', 'f', 'a', 'b', 'd'])
