    def test_symmetrizing(self):
        lctr = mticker.AsinhLocator(linear_width=1, numticks=3,
                                    symthresh=0.25, base=0)
        lctr.create_dummy_axis()

        lctr.axis.set_view_interval(-1, 2)
        assert_almost_equal(lctr(), [-1, 0, 2])

        lctr.axis.set_view_interval(-1, 0.9)
        assert_almost_equal(lctr(), [-1, 0, 1])

        lctr.axis.set_view_interval(-0.85, 1.05)
        assert_almost_equal(lctr(), [-1, 0, 1])

        lctr.axis.set_view_interval(1, 1.1)
        assert_almost_equal(lctr(), [1, 1.05, 1.1])
