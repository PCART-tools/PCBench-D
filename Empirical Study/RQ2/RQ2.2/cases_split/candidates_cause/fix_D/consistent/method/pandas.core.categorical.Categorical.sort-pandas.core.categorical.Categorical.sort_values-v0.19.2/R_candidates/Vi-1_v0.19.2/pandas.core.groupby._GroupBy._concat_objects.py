    def _concat_objects(self, keys, values, not_indexed_same=False):
        from pandas.tools.merge import concat

        def reset_identity(values):
            # reset the identities of the components
            # of the values to prevent aliasing
            for v in values:
                if v is not None:
                    ax = v._get_axis(self.axis)
                    ax._reset_identity()
            return values

        if not not_indexed_same:
            result = concat(values, axis=self.axis)
            ax = self._selected_obj._get_axis(self.axis)

            if isinstance(result, Series):
                result = result.reindex(ax)
            else:

                # this is a very unfortunate situation
                # we have a multi-index that is NOT lexsorted
                # and we have a result which is duplicated
                # we can't reindex, so we resort to this
                # GH 14776
                if isinstance(ax, MultiIndex) and not ax.is_unique:
                    result = result.take(result.index.get_indexer_for(
                        ax.values).unique(), axis=self.axis)
                else:
                    result = result.reindex_axis(ax, axis=self.axis)

        elif self.group_keys:

            values = reset_identity(values)
            if self.as_index:

                # possible MI return case
                group_keys = keys
                group_levels = self.grouper.levels
                group_names = self.grouper.names

                result = concat(values, axis=self.axis, keys=group_keys,
                                levels=group_levels, names=group_names)
            else:

                # GH5610, returns a MI, with the first level being a
                # range index
                keys = list(range(len(values)))
                result = concat(values, axis=self.axis, keys=keys)
        else:
            values = reset_identity(values)
            result = concat(values, axis=self.axis)

        if (isinstance(result, Series) and
                getattr(self, 'name', None) is not None):

            result.name = self.name

        return result
