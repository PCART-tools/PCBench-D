    def _wrap_generic_output(self, result, obj):
        result_index = self.grouper.levels[0]

        if result:
            if self.axis == 0:
                result = DataFrame(result, index=obj.columns,
                                   columns=result_index).T
            else:
                result = DataFrame(result, index=obj.index,
                                   columns=result_index)
        else:
            result = DataFrame(result)

        return result
