    def to_html(
        self,
        buf: FilePathOrBuffer[str] | None = None,
        *,
        table_uuid: str | None = None,
        table_attributes: str | None = None,
        encoding: str | None = None,
        doctype_html: bool = False,
        exclude_styles: bool = False,
    ):
        """
        Write Styler to a file, buffer or string in HTML-CSS format.

        .. versionadded:: 1.3.0

        Parameters
        ----------
        buf : str, Path, or StringIO-like, optional, default None
            Buffer to write to. If ``None``, the output is returned as a string.
        table_uuid : str, optional
            Id attribute assigned to the <table> HTML element in the format:

            ``<table id="T_<table_uuid>" ..>``

            If not given uses Styler's initially assigned value.
        table_attributes : str, optional
            Attributes to assign within the `<table>` HTML element in the format:

            ``<table .. <table_attributes> >``

            If not given defaults to Styler's preexisting value.
        encoding : str, optional
            Character encoding setting for file output, and HTML meta tags,
            defaults to "utf-8" if None.
        doctype_html : bool, default False
            Whether to output a fully structured HTML file including all
            HTML elements, or just the core ``<style>`` and ``<table>`` elements.
        exclude_styles : bool, default False
            Whether to include the ``<style>`` element and all associated element
            ``class`` and ``id`` identifiers, or solely the ``<table>`` element without
            styling identifiers.

        Returns
        -------
        str or None
            If `buf` is None, returns the result as a string. Otherwise returns `None`.

        See Also
        --------
        DataFrame.to_html: Write a DataFrame to a file, buffer or string in HTML format.
        """
        if table_uuid:
            self.set_uuid(table_uuid)

        if table_attributes:
            self.set_table_attributes(table_attributes)

        # Build HTML string..
        html = self.render(
            exclude_styles=exclude_styles,
            encoding=encoding if encoding else "utf-8",
            doctype_html=doctype_html,
        )

        return save_to_buffer(
            html, buf=buf, encoding=(encoding if buf is not None else None)
        )
