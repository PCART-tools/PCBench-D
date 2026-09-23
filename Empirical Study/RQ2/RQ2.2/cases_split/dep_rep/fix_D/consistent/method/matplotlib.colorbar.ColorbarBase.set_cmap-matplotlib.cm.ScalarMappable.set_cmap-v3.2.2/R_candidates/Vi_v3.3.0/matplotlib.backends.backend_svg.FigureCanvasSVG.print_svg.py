    def print_svg(self, filename, *args, **kwargs):
        """
        Parameters
        ----------
        filename : str or path-like or file-like
            Output target; if a string, a file will be opened for writing.
        metadata : Dict[str, Any], optional
            Metadata in the SVG file defined as key-value pairs of strings,
            datetimes, or lists of strings, e.g., ``{'Creator': 'My software',
            'Contributor': ['Me', 'My Friend'], 'Title': 'Awesome'}``.

            The standard keys and their value types are:

            * *str*: ``'Coverage'``, ``'Description'``, ``'Format'``,
              ``'Identifier'``, ``'Language'``, ``'Relation'``, ``'Source'``,
              ``'Title'``, and ``'Type'``.
            * *str* or *list of str*: ``'Contributor'``, ``'Creator'``,
              ``'Keywords'``, ``'Publisher'``, and ``'Rights'``.
            * *str*, *date*, *datetime*, or *tuple* of same: ``'Date'``. If a
              non-*str*, then it will be formatted as ISO 8601.

            Values have been predefined for ``'Creator'``, ``'Date'``,
            ``'Format'``, and ``'Type'``. They can be removed by setting them
            to `None`.

            Information is encoded as `Dublin Core Metadata`__.

            .. _DC: https://www.dublincore.org/specifications/dublin-core/

            __ DC_
        """
        with cbook.open_file_cm(filename, "w", encoding="utf-8") as fh:

            filename = getattr(fh, 'name', '')
            if not isinstance(filename, str):
                filename = ''

            if cbook.file_requires_unicode(fh):
                detach = False
            else:
                fh = TextIOWrapper(fh, 'utf-8')
                detach = True

            self._print_svg(filename, fh, **kwargs)

            # Detach underlying stream from wrapper so that it remains open in
            # the caller.
            if detach:
                fh.detach()
