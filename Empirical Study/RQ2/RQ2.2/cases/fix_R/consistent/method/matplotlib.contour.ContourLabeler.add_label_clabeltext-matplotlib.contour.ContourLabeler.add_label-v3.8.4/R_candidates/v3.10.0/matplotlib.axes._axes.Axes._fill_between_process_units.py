    def _fill_between_process_units(self, ind_dir, dep_dir, ind, dep1, dep2, **kwargs):
        """Handle united data, such as dates."""
        return map(np.ma.masked_invalid, self._process_unit_info(
            [(ind_dir, ind), (dep_dir, dep1), (dep_dir, dep2)], kwargs))
