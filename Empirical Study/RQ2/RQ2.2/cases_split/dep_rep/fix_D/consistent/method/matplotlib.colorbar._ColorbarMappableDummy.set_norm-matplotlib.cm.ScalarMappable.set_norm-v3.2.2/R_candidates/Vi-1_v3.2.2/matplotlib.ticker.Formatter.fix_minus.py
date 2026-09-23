    def fix_minus(self, s):
        """
        Some classes may want to replace a hyphen for minus with the
        proper unicode symbol (U+2212) for typographical correctness.
        The default is to not replace it.

        Note, if you use this method, e.g., in :meth:`format_data` or
        call, you probably don't want to use it for
        :meth:`format_data_short` since the toolbar uses this for
        interactive coord reporting and I doubt we can expect GUIs
        across platforms will handle the unicode correctly.  So for
        now the classes that override :meth:`fix_minus` should have an
        explicit :meth:`format_data_short` method
        """
        return s
