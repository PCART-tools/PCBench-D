    @Substitution(name='groupby')
    @Appender(_doc_template)
    def size(self):
        """Compute group sizes"""
        result = self.grouper.size()

        if isinstance(self.obj, Series):
            result.name = getattr(self.obj, 'name', None)
        return result
