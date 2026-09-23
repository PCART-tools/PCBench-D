    @abstractmethod
    def render(
        self,
        *,
        buf: IO[str] | None,
        max_cols: int | None,
        verbose: bool | None,
        show_counts: bool | None,
    ) -> None:
        """
        Print a concise summary of a %(klass)s.

        This method prints information about a %(klass)s including
        the index dtype%(type_sub)s, non-null values and memory usage.
        %(version_added_sub)s\

        Parameters
        ----------
        data : %(klass)s
            %(klass)s to print information about.
        verbose : bool, optional
            Whether to print the full summary. By default, the setting in
            ``pandas.options.display.max_info_columns`` is followed.
        buf : writable buffer, defaults to sys.stdout
            Where to send the output. By default, the output is printed to
            sys.stdout. Pass a writable buffer if you need to further process
            the output.
        %(max_cols_sub)s
        memory_usage : bool, str, optional
            Specifies whether total memory usage of the %(klass)s
            elements (including the index) should be displayed. By default,
            this follows the ``pandas.options.display.memory_usage`` setting.

            True always show memory usage. False never shows memory usage.
            A value of 'deep' is equivalent to "True with deep introspection".
            Memory usage is shown in human-readable units (base-2
            representation). Without deep introspection a memory estimation is
            made based in column dtype and number of rows assuming values
            consume the same memory amount for corresponding dtypes. With deep
            memory introspection, a real memory usage calculation is performed
            at the cost of computational resources.
        %(show_counts_sub)s

        Returns
        -------
        None
            This method prints a summary of a %(klass)s and returns None.

        See Also
        --------
        %(see_also_sub)s

        Examples
        --------
        %(examples_sub)s
        """
