    def _wrap_transformed_output(self, output, names=None):
        return self._wrap_output(output=output,
                                 index=self.obj.index,
                                 names=names)
