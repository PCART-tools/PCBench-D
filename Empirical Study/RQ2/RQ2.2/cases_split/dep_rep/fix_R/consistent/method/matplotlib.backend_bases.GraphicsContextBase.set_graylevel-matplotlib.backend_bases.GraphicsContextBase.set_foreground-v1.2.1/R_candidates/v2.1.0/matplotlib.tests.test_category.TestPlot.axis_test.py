    def axis_test(self, axis, ticks, labels, unit_data):
        np.testing.assert_array_equal(axis.get_majorticklocs(), ticks)
        assert lt(axis.get_majorticklabels()) == labels
        np.testing.assert_array_equal(axis.unit_data.locs, unit_data.locs)
        assert axis.unit_data.seq == unit_data.seq
