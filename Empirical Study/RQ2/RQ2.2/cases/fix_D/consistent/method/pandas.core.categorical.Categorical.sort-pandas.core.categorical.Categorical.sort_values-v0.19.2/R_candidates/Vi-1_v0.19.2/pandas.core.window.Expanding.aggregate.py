    @Substitution(name='expanding')
    @Appender(SelectionMixin._see_also_template)
    @Appender(SelectionMixin._agg_doc)
    def aggregate(self, arg, *args, **kwargs):
        return super(Expanding, self).aggregate(arg, *args, **kwargs)
