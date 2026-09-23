    def _reindex_output(self, result):
        """
        if we have categorical groupers, then we want to make sure that
        we have a fully reindex-output to the levels. These may have not participated in
        the groupings (e.g. may have all been nan groups)

        This can re-expand the output space
        """
        groupings = self.grouper.groupings
        if groupings is None:
            return result
        elif len(groupings) == 1:
            return result
        elif not any([isinstance(ping.grouper, (Categorical, CategoricalIndex))
                      for ping in groupings]):
            return result

        levels_list = [ ping.group_index for ping in groupings ]
        index = MultiIndex.from_product(levels_list, names=self.grouper.names)
        d = { self.obj._get_axis_name(self.axis) : index, 'copy' : False }
        return result.reindex(**d).sortlevel(axis=self.axis)
