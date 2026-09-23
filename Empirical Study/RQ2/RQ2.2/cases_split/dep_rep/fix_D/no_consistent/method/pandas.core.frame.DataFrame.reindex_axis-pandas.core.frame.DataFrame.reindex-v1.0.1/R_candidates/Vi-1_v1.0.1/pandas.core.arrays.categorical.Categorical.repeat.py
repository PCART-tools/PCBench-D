    @Substitution(klass="Categorical")
    @Appender(_extension_array_shared_docs["repeat"])
    def repeat(self, repeats, axis=None):
        nv.validate_repeat(tuple(), dict(axis=axis))
        codes = self._codes.repeat(repeats)
        return self._constructor(values=codes, dtype=self.dtype, fastpath=True)
