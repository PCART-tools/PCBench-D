    def _reindex_output(self, result):
        """
        if we have categorical groupers, then we want to make sure that
        we have a fully reindex-output to the levels. These may have not
        participated in the groupings (e.g. may have all been
        nan groups)

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

        levels_list = [ping.group_index for ping in groupings]
        index, _ = MultiIndex.from_product(
            levels_list, names=self.grouper.names).sortlevel()

        if self.as_index:
            d = {self.obj._get_axis_name(self.axis): index, 'copy': False}
            return result.reindex(**d)

        # GH 13204
        # Here, the categorical in-axis groupers, which need to be fully
        # expanded, are columns in `result`. An idea is to do:
        # result = result.set_index(self.grouper.names)
        #                .reindex(index).reset_index()
        # but special care has to be taken because of possible not-in-axis
        # groupers.
        # So, we manually select and drop the in-axis grouper columns,
        # reindex `result`, and then reset the in-axis grouper columns.

        # Select in-axis groupers
        in_axis_grps = [(i, ping.name) for (i, ping)
                        in enumerate(groupings) if ping.in_axis]
        g_nums, g_names = zip(*in_axis_grps)

        result = result.drop(labels=list(g_names), axis=1)

        # Set a temp index and reindex (possibly expanding)
        result = result.set_index(self.grouper.result_index
                                  ).reindex(index, copy=False)

        # Reset in-axis grouper columns
        # (using level numbers `g_nums` because level names may not be unique)
        result = result.reset_index(level=g_nums)

        return result.reset_index(drop=True)
