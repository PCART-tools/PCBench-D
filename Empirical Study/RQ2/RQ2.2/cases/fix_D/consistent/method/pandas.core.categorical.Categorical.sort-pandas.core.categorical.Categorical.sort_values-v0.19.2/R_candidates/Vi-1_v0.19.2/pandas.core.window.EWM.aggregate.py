    @Substitution(name='ewm')
    @Appender(SelectionMixin._see_also_template)
    @Appender(SelectionMixin._agg_doc)
    def aggregate(self, arg, *args, **kwargs):
        return super(EWM, self).aggregate(arg, *args, **kwargs)
