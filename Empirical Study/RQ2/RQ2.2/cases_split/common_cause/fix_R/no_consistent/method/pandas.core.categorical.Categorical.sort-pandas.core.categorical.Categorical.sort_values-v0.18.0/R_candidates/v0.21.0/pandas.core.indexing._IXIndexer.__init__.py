    def __init__(self, obj, name):

        _ix_deprecation_warning = textwrap.dedent("""
            .ix is deprecated. Please use
            .loc for label based indexing or
            .iloc for positional indexing

            See the documentation here:
            http://pandas.pydata.org/pandas-docs/stable/indexing.html#ix-indexer-is-deprecated""")  # noqa

        warnings.warn(_ix_deprecation_warning,
                      DeprecationWarning, stacklevel=3)
        super(_IXIndexer, self).__init__(obj, name)
