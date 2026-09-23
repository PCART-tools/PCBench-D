    @final
    def _concat_objects(
        self,
        values,
        not_indexed_same: bool = False,
        is_transform: bool = False,
    ):
        from pandas.core.reshape.concat import concat

        if self.group_keys and not is_transform:
            if self.as_index:
                # possible MI return case
                group_keys = self.grouper.result_index
                group_levels = self.grouper.levels
                group_names = self.grouper.names

                result = concat(
                    values,
                    axis=self.axis,
                    keys=group_keys,
                    levels=group_levels,
                    names=group_names,
                    sort=False,
                )
            else:
                # GH5610, returns a MI, with the first level being a
                # range index
                keys = list(range(len(values)))
                result = concat(values, axis=self.axis, keys=keys)

        elif not not_indexed_same:
            result = concat(values, axis=self.axis)

            ax = self._selected_obj._get_axis(self.axis)
            if self.dropna:
                labels = self.grouper.group_info[0]
                mask = labels != -1
                ax = ax[mask]

            # this is a very unfortunate situation
            # we can't use reindex to restore the original order
            # when the ax has duplicates
            # so we resort to this
            # GH 14776, 30667
            # TODO: can we re-use e.g. _reindex_non_unique?
            if ax.has_duplicates and not result.axes[self.axis].equals(ax):
                # e.g. test_category_order_transformer
                target = algorithms.unique1d(ax._values)
                indexer, _ = result.index.get_indexer_non_unique(target)
                result = result.take(indexer, axis=self.axis)
            else:
                result = result.reindex(ax, axis=self.axis, copy=False)

        else:
            result = concat(values, axis=self.axis)

        if self.obj.ndim == 1:
            name = self.obj.name
        elif is_hashable(self._selection):
            name = self._selection
        else:
            name = None

        if isinstance(result, Series) and name is not None:
            result.name = name

        return result
