    def test_subs(self):
        sym = mticker.SymmetricalLogLocator(base=10, linthresh=1, subs=[2.0, 4.0])
        sym.create_dummy_axis()
        sym.axis.set_view_interval(-10, 10)
        assert (sym() == [-20., -40.,  -2.,  -4.,   0.,   2.,   4.,  20.,  40.]).all()
