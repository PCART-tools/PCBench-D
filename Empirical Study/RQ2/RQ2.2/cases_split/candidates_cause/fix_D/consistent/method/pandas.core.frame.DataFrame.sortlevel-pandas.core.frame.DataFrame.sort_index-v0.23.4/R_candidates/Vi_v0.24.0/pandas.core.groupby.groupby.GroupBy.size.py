    @Substitution(name='groupby')
    @Appender(_common_see_also)
    def size(self):
        """
        Compute group sizes.
        """
        result = self.grouper.size()

        if isinstance(self.obj, Series):
            result.name = getattr(self.obj, 'name', None)
        return result
