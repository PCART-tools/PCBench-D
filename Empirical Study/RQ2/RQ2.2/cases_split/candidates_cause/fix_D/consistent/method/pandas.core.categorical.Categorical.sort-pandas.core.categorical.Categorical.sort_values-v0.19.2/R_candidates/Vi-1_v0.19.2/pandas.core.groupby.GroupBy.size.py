    @Substitution(name='groupby')
    @Appender(_doc_template)
    def size(self):
        """Compute group sizes"""
        return self.grouper.size()
