    @Substitution(klass='Resampler',
                  versionadded='.. versionadded:: 0.23.0',
                  examples="""
    >>> df = pd.DataFrame({'A': [1, 2, 3, 4]},
    ...                   index=pd.date_range('2012-08-02', periods=4))
    >>> df
                A
    2012-08-02  1
    2012-08-03  2
    2012-08-04  3
    2012-08-05  4

    To get the difference between each 2-day period's maximum and minimum
    value in one pass, you can do

    >>> df.resample('2D').pipe(lambda x: x.max() - x.min())
                A
    2012-08-02  1
    2012-08-04  1
    """)
    @Appender(_pipe_template)
    def pipe(self, func, *args, **kwargs):
        return super(Resampler, self).pipe(func, *args, **kwargs)
