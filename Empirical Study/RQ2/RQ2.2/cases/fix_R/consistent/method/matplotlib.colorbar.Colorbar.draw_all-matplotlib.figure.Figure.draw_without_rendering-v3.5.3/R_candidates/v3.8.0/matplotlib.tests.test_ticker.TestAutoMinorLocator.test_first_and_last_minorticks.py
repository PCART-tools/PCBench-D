    def test_first_and_last_minorticks(self):
        """
        Test that first and last minor tick appear as expected.
        """
        # This test is related to issue #22331
        fig, ax = plt.subplots()
        ax.set_xlim(-1.9, 1.9)
        ax.xaxis.set_minor_locator(mticker.AutoMinorLocator())
        test_value = np.array([-1.9, -1.8, -1.7, -1.6, -1.4, -1.3, -1.2, -1.1,
                               -0.9, -0.8, -0.7, -0.6, -0.4, -0.3, -0.2, -0.1,
                               0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9, 1.1,
                               1.2, 1.3, 1.4, 1.6, 1.7, 1.8, 1.9])
        assert_almost_equal(ax.xaxis.get_ticklocs(minor=True), test_value)

        ax.set_xlim(-5, 5)
        test_value = np.array([-5.0, -4.5, -3.5, -3.0, -2.5, -1.5, -1.0, -0.5,
                               0.5, 1.0, 1.5, 2.5, 3.0, 3.5, 4.5, 5.0])
        assert_almost_equal(ax.xaxis.get_ticklocs(minor=True), test_value)
