    @Substitution(name='rolling')
    @Appender(SelectionMixin._see_also_template)
    @Appender(SelectionMixin._agg_doc)
    def aggregate(self, arg, *args, **kwargs):
        return super(Rolling, self).aggregate(arg, *args, **kwargs)
