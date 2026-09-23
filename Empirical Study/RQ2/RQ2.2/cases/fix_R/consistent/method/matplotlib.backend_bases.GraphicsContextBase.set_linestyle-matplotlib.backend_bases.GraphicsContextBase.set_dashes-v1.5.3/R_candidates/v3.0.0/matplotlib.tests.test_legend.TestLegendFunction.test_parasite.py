    def test_parasite(self):
        from mpl_toolkits.axes_grid1 import host_subplot

        host = host_subplot(111)
        par = host.twinx()

        p1, = host.plot([0, 1, 2], [0, 1, 2], label="Density")
        p2, = par.plot([0, 1, 2], [0, 3, 2], label="Temperature")

        with mock.patch('matplotlib.legend.Legend') as Legend:
            leg = plt.legend()
        Legend.assert_called_with(host, [p1, p2],
                ['Density', 'Temperature'])
