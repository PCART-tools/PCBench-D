    def _wrap_aggregated_output(self, output, names=None):
        # sort of a kludge
        output = output[self.name]
        index = self.grouper.result_index

        if names is not None:
            return DataFrame(output, index=index, columns=names)
        else:
            return Series(output, index=index, name=self.name)
