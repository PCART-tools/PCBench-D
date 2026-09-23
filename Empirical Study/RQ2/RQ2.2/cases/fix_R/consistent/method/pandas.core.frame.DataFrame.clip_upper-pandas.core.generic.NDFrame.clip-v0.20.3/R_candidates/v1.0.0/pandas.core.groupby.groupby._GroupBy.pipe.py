    @Substitution(
        klass="GroupBy",
        versionadded=".. versionadded:: 0.21.0",
        examples="""\
>>> df = pd.DataFrame({'A': 'a b a b'.split(), 'B': [1, 2, 3, 4]})
>>> df
   A  B
0  a  1
1  b  2
2  a  3
3  b  4

To get the difference between each groups maximum and minimum value in one
pass, you can do

>>> df.groupby('A').pipe(lambda x: x.max() - x.min())
   B
A
a  2
b  2""",
    )
    @Appender(_pipe_template)
    def pipe(self, func, *args, **kwargs):
        return com.pipe(self, func, *args, **kwargs)
