    @final
    def _concat_objects(self, values, not_indexed_same: bool = False):
        from pandas.core.reshape.concat import concat

        def reset_identity(values):
            # reset the identities of the components
            # of the values to prevent aliasing
            for v in com.not_none(*values):
                ax = v._get_axis(self.axis)
                ax._reset_identity()
            return values

        if not not_indexed_same:
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
            if ax.has_duplicates and not result.axes[self.axis].equals(ax):
                indexer, _ = result.index.get_indexer_non_unique(ax._values)
                indexer = algorithms.unique1d(indexer)
                result = result.take(indexer, axis=self.axis)
            else:
                result = result.reindex(ax, axis=self.axis, copy=False)

        elif self.group_keys:

            values = reset_identity(values)
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
        else:
            values = reset_identity(values)
            result = concat(values, axis=self.axis)

        name = self.obj.name if self.obj.ndim == 1 else self._selection
        if isinstance(result, Series) and name is not None:

            result.name = name

        return result
