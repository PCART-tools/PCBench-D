    def _concat_objects(self, keys, values, not_indexed_same=False):
        from pandas.tools.merge import concat

        if not not_indexed_same:
            result = concat(values, axis=self.axis)
            ax = self._selected_obj._get_axis(self.axis)

            if isinstance(result, Series):
                result = result.reindex(ax)
            else:
                result = result.reindex_axis(ax, axis=self.axis)

        elif self.group_keys:

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
            result = concat(values, axis=self.axis)

        return result
