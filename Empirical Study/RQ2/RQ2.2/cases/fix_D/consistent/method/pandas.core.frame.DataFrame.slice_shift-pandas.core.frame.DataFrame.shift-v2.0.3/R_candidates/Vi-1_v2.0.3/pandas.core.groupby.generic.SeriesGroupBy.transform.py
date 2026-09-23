    @Substitution(klass="Series", example=__examples_series_doc)
    @Appender(_transform_template)
    def transform(self, func, *args, engine=None, engine_kwargs=None, **kwargs):
        return self._transform(
            func, *args, engine=engine, engine_kwargs=engine_kwargs, **kwargs
        )
