    def concat(self, other: Styler) -> Styler:
        """
        Append another Styler to combine the output into a single table.

        .. versionadded:: 1.5.0

        Parameters
        ----------
        other : Styler
            The other Styler object which has already been styled and formatted. The
            data for this Styler must have the same columns as the original, and the
            number of index levels must also be the same to render correctly.

        Returns
        -------
        Styler

        Notes
        -----
        The purpose of this method is to extend existing styled dataframes with other
        metrics that may be useful but may not conform to the original's structure.
        For example adding a sub total row, or displaying metrics such as means,
        variance or counts.

        Styles that are applied using the ``apply``, ``applymap``, ``apply_index``
        and ``applymap_index``, and formatting applied with ``format`` and
        ``format_index`` will be preserved.

        .. warning::
            Only the output methods ``to_html``, ``to_string`` and ``to_latex``
            currently work with concatenated Stylers.

            Other output methods, including ``to_excel``, **do not** work with
            concatenated Stylers.

        The following should be noted:

          - ``table_styles``, ``table_attributes``, ``caption`` and ``uuid`` are all
            inherited from the original Styler and not ``other``.
          - hidden columns and hidden index levels will be inherited from the
            original Styler
          - ``css`` will be inherited from the original Styler, and the value of
            keys ``data``, ``row_heading`` and ``row`` will be prepended with
            ``foot0_``. If more concats are chained, their styles will be prepended
            with ``foot1_``, ''foot_2'', etc., and if a concatenated style have
            another concatanated style, the second style will be prepended with
            ``foot{parent}_foot{child}_``.

        A common use case is to concatenate user defined functions with
        ``DataFrame.agg`` or with described statistics via ``DataFrame.describe``.
        See examples.

        Examples
        --------
        A common use case is adding totals rows, or otherwise, via methods calculated
        in ``DataFrame.agg``.

        >>> df = DataFrame([[4, 6], [1, 9], [3, 4], [5, 5], [9,6]],
        ...                columns=["Mike", "Jim"],
        ...                index=["Mon", "Tue", "Wed", "Thurs", "Fri"])
        >>> styler = df.style.concat(df.agg(["sum"]).style)  # doctest: +SKIP

        .. figure:: ../../_static/style/footer_simple.png

        Since the concatenated object is a Styler the existing functionality can be
        used to conditionally format it as well as the original.

        >>> descriptors = df.agg(["sum", "mean", lambda s: s.dtype])
        >>> descriptors.index = ["Total", "Average", "dtype"]
        >>> other = (descriptors.style
        ...          .highlight_max(axis=1, subset=(["Total", "Average"], slice(None)))
        ...          .format(subset=("Average", slice(None)), precision=2, decimal=",")
        ...          .applymap(lambda v: "font-weight: bold;"))
        >>> styler = (df.style
        ...             .highlight_max(color="salmon")
        ...             .set_table_styles([{"selector": ".foot_row0",
        ...                                 "props": "border-top: 1px solid black;"}]))
        >>> styler.concat(other)  # doctest: +SKIP

        .. figure:: ../../_static/style/footer_extended.png

        When ``other`` has fewer index levels than the original Styler it is possible
        to extend the index in ``other``, with placeholder levels.

        >>> df = DataFrame([[1], [2]], index=pd.MultiIndex.from_product([[0], [1, 2]]))
        >>> descriptors = df.agg(["sum"])
        >>> descriptors.index = pd.MultiIndex.from_product([[""], descriptors.index])
        >>> df.style.concat(descriptors.style)  # doctest: +SKIP
        """
        if not isinstance(other, Styler):
            raise TypeError("`other` must be of type `Styler`")
        if not self.data.columns.equals(other.data.columns):
            raise ValueError("`other.data` must have same columns as `Styler.data`")
        if not self.data.index.nlevels == other.data.index.nlevels:
            raise ValueError(
                "number of index levels must be same in `other` "
                "as in `Styler`. See documentation for suggestions."
            )
        self.concatenated.append(other)
        return self
