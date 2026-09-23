    def _wrap_generic_output(self, result, obj):
        result_index = self.grouper.levels[0]

        if self.axis == 0:
            return DataFrame(result, index=obj.columns,
                             columns=result_index).T
        else:
            return DataFrame(result, index=obj.index,
                             columns=result_index)
