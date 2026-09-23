    def _python_apply_general(self, f):
        keys, values, mutated = self.grouper.apply(f, self.obj, self.axis)

        return self._wrap_applied_output(keys, values,
                                         not_indexed_same=mutated)
