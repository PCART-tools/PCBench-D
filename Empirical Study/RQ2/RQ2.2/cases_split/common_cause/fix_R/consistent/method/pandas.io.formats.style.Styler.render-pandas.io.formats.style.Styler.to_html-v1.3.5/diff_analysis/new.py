    def render(
        self,
        sparse_index: bool | None = None,
        sparse_columns: bool | None = None,
        **kwargs,
    ) -> str:
        """
        Render the ``Styler`` including all applied styles to HTML.

        .. deprecated:: 1.4.0

        Parameters
        ----------
        sparse_index : bool, optional
            Whether to sparsify the display of a hierarchical index. Setting to False
            will display each explicit level element in a hierarchical key for each row.
            Defaults to ``pandas.options.styler.sparse.index`` value.
        sparse_columns : bool, optional
            Whether to sparsify the display of a hierarchical index. Setting to False
            will display each explicit level element in a hierarchical key for each row.
            Defaults to ``pandas.options.styler.sparse.columns`` value.
        **kwargs
            Any additional keyword arguments are passed
            through to ``self.template.render``.
            This is useful when you need to provide
            additional variables for a custom template.

        Returns
        -------
        rendered : str
            The rendered HTML.

        Notes
        -----
        This method is deprecated in favour of ``Styler.to_html``.

        Styler objects have defined the ``_repr_html_`` method
        which automatically calls ``self.to_html()`` when it's the
        last item in a Notebook cell.

        When calling ``Styler.render()`` directly, wrap the result in
        ``IPython.display.HTML`` to view the rendered HTML in the notebook.

        Pandas uses the following keys in render. Arguments passed
        in ``**kwargs`` take precedence, so think carefully if you want
        to override them:

        * head
        * cellstyle
        * body
        * uuid
        * table_styles
        * caption
        * table_attributes
        """
        warnings.warn(
            "this method is deprecated in favour of `Styler.to_html()`",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        if sparse_index is None:
            sparse_index = get_option("styler.sparse.index")
        if sparse_columns is None:
            sparse_columns = get_option("styler.sparse.columns")
        return self._render_html(sparse_index, sparse_columns, **kwargs)
