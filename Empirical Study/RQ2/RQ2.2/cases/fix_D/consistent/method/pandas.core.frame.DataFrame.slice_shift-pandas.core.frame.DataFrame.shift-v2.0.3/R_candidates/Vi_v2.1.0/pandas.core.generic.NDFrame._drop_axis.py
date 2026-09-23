    @final
    def _drop_axis(
        self,
        labels,
        axis,
        level=None,
        errors: IgnoreRaise = "raise",
        only_slice: bool_t = False,
    ) -> Self:
        """
        Drop labels from specified axis. Used in the ``drop`` method
        internally.

        Parameters
        ----------
        labels : single label or list-like
        axis : int or axis name
        level : int or level name, default None
            For MultiIndex
        errors : {'ignore', 'raise'}, default 'raise'
            If 'ignore', suppress error and existing labels are dropped.
        only_slice : bool, default False
            Whether indexing along columns should be view-only.

        """
        axis_num = self._get_axis_number(axis)
        axis = self._get_axis(axis)

        if axis.is_unique:
            if level is not None:
                if not isinstance(axis, MultiIndex):
                    raise AssertionError("axis must be a MultiIndex")
                new_axis = axis.drop(labels, level=level, errors=errors)
            else:
                new_axis = axis.drop(labels, errors=errors)
            indexer = axis.get_indexer(new_axis)

        # Case for non-unique axis
        else:
            is_tuple_labels = is_nested_list_like(labels) or isinstance(labels, tuple)
            labels = ensure_object(common.index_labels_to_array(labels))
            if level is not None:
                if not isinstance(axis, MultiIndex):
                    raise AssertionError("axis must be a MultiIndex")
                mask = ~axis.get_level_values(level).isin(labels)

                # GH 18561 MultiIndex.drop should raise if label is absent
                if errors == "raise" and mask.all():
                    raise KeyError(f"{labels} not found in axis")
            elif (
                isinstance(axis, MultiIndex)
                and labels.dtype == "object"
                and not is_tuple_labels
            ):
                # Set level to zero in case of MultiIndex and label is string,
                #  because isin can't handle strings for MultiIndexes GH#36293
                # In case of tuples we get dtype object but have to use isin GH#42771
                mask = ~axis.get_level_values(0).isin(labels)
            else:
                mask = ~axis.isin(labels)
                # Check if label doesn't exist along axis
                labels_missing = (axis.get_indexer_for(labels) == -1).any()
                if errors == "raise" and labels_missing:
                    raise KeyError(f"{labels} not found in axis")

            if isinstance(mask.dtype, ExtensionDtype):
                # GH#45860
                mask = mask.to_numpy(dtype=bool)

            indexer = mask.nonzero()[0]
            new_axis = axis.take(indexer)

        bm_axis = self.ndim - axis_num - 1
        new_mgr = self._mgr.reindex_indexer(
            new_axis,
            indexer,
            axis=bm_axis,
            allow_dups=True,
            copy=None,
            only_slice=only_slice,
        )
        result = self._constructor_from_mgr(new_mgr, axes=new_mgr.axes)
        if self.ndim == 1:
            result._name = self.name

        return result.__finalize__(self)
