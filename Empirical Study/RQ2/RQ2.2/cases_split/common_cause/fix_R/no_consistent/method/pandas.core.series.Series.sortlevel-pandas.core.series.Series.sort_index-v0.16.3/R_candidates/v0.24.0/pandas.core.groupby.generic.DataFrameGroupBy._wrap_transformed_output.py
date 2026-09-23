    def _wrap_transformed_output(self, output, names=None):
        return DataFrame(output, index=self.obj.index)
