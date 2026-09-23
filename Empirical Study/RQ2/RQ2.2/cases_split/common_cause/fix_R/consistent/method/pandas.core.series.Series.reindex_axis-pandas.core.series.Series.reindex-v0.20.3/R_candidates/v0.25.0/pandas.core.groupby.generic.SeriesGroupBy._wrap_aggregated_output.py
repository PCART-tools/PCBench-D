    def _wrap_aggregated_output(self, output, names=None):
        result = self._wrap_output(
            output=output, index=self.grouper.result_index, names=names
        )
        return self._reindex_output(result)._convert(datetime=True)
