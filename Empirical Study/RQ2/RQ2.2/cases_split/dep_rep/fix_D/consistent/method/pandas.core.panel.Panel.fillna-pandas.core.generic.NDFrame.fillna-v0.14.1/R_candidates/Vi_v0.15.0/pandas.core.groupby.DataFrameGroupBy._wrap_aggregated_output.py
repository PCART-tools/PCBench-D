    def _wrap_aggregated_output(self, output, names=None):
        agg_axis = 0 if self.axis == 1 else 1
        agg_labels = self._obj_with_exclusions._get_axis(agg_axis)

        output_keys = self._decide_output_index(output, agg_labels)

        if not self.as_index:
            result = DataFrame(output, columns=output_keys)
            group_levels = self.grouper.get_group_levels()
            zipped = zip(self.grouper.names, group_levels)

            for i, (name, labels) in enumerate(zipped):
                result.insert(i, name, labels)
            result = result.consolidate()
        else:
            index = self.grouper.result_index
            result = DataFrame(output, index=index, columns=output_keys)

        if self.axis == 1:
            result = result.T

        return self._reindex_output(result).convert_objects()
