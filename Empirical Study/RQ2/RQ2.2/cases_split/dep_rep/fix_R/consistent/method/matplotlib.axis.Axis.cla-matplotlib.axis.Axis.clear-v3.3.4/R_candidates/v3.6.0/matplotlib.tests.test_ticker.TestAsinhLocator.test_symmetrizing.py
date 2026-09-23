    def test_symmetrizing(self):
        class DummyAxis:
            bounds = (-1, 1)
            @classmethod
            def get_view_interval(cls): return cls.bounds

        lctr = mticker.AsinhLocator(linear_width=1, numticks=3,
                                    symthresh=0.25, base=0)
        lctr.axis = DummyAxis

        DummyAxis.bounds = (-1, 2)
        assert_almost_equal(lctr(), [-1, 0, 2])

        DummyAxis.bounds = (-1, 0.9)
        assert_almost_equal(lctr(), [-1, 0, 1])

        DummyAxis.bounds = (-0.85, 1.05)
        assert_almost_equal(lctr(), [-1, 0, 1])

        DummyAxis.bounds = (1, 1.1)
        assert_almost_equal(lctr(), [1, 1.05, 1.1])
