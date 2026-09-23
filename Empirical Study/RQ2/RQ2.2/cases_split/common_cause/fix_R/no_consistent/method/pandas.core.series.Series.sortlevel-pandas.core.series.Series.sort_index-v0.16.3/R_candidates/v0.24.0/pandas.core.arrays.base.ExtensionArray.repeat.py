    @Substitution(klass='ExtensionArray')
    @Appender(_extension_array_shared_docs['repeat'])
    def repeat(self, repeats, axis=None):
        nv.validate_repeat(tuple(), dict(axis=axis))
        ind = np.arange(len(self)).repeat(repeats)
        return self.take(ind)
