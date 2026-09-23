    def to_panel(self):
        """
        Transform long (stacked) format (DataFrame) into wide (3D, Panel)
        format.

        Currently the index of the DataFrame must be a 2-level MultiIndex. This
        may be generalized later

        Returns
        -------
        panel : Panel
        """
        # only support this kind for now
        if (not isinstance(self.index, MultiIndex) or  # pragma: no cover
                len(self.index.levels) != 2):
            raise NotImplementedError('Only 2-level MultiIndex are supported.')

        if not self.index.is_unique:
            raise ValueError("Can't convert non-uniquely indexed "
                             "DataFrame to Panel")

        self._consolidate_inplace()

        # minor axis must be sorted
        if self.index.lexsort_depth < 2:
            selfsorted = self.sort_index(level=0)
        else:
            selfsorted = self

        major_axis, minor_axis = selfsorted.index.levels
        major_labels, minor_labels = selfsorted.index.labels
        shape = len(major_axis), len(minor_axis)

        # preserve names, if any
        major_axis = major_axis.copy()
        major_axis.name = self.index.names[0]

        minor_axis = minor_axis.copy()
        minor_axis.name = self.index.names[1]

        # create new axes
        new_axes = [selfsorted.columns, major_axis, minor_axis]

        # create new manager
        new_mgr = selfsorted._data.reshape_nd(axes=new_axes,
                                              labels=[major_labels,
                                                      minor_labels],
                                              shape=shape,
                                              ref_items=selfsorted.columns)

        return self._constructor_expanddim(new_mgr)
