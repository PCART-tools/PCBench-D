    @deprecate_renamed_parameter("has_header", "include_header", version="0.19.13")
    def write_excel(
        self,
        workbook: Workbook | BytesIO | Path | str | None = None,
        worksheet: str | None = None,
        *,
        position: tuple[int, int] | str = "A1",
        table_style: str | dict[str, Any] | None = None,
        table_name: str | None = None,
        column_formats: ColumnFormatDict | None = None,
        dtype_formats: dict[OneOrMoreDataTypes, str] | None = None,
        conditional_formats: ConditionalFormatDict | None = None,
        header_format: dict[str, Any] | None = None,
        column_totals: ColumnTotalsDefinition | None = None,
        column_widths: ColumnWidthsDefinition | None = None,
        row_totals: RowTotalsDefinition | None = None,
        row_heights: dict[int | tuple[int, ...], int] | int | None = None,
        sparklines: dict[str, Sequence[str] | dict[str, Any]] | None = None,
        formulas: dict[str, str | dict[str, str]] | None = None,
        float_precision: int = 3,
        include_header: bool = True,
        autofilter: bool = True,
        autofit: bool = False,
        hidden_columns: Sequence[str] | SelectorType | None = None,
        hide_gridlines: bool = False,
        sheet_zoom: int | None = None,
        freeze_panes: (
            str
            | tuple[int, int]
            | tuple[str, int, int]
            | tuple[int, int, int, int]
            | None
        ) = None,
    ) -> Workbook:
        """
        Write frame data to a table in an Excel workbook/worksheet.

        Parameters
        ----------
        workbook : Workbook
            String name or path of the workbook to create, BytesIO object to write
            into, or an open `xlsxwriter.Workbook` object that has not been closed.
            If None, writes to a `dataframe.xlsx` workbook in the working directory.
        worksheet : str
            Name of target worksheet; if None, writes to "Sheet1" when creating a new
            workbook (note that writing to an existing workbook requires a valid
            existing -or new- worksheet name).
        position : {str, tuple}
            Table position in Excel notation (eg: "A1"), or a (row,col) integer tuple.
        table_style : {str, dict}
            A named Excel table style, such as "Table Style Medium 4", or a dictionary
            of `{"key":value,}` options containing one or more of the following keys:
            "style", "first_column", "last_column", "banded_columns, "banded_rows".
        table_name : str
            Name of the output table object in the worksheet; can then be referred to
            in the sheet by formulae/charts, or by subsequent `xlsxwriter` operations.
        column_formats : dict
            A `{colname(s):str,}` or `{selector:str,}` dictionary for applying an
            Excel format string to the given columns. Formats defined here (such as
            "dd/mm/yyyy", "0.00%", etc) will override any defined in `dtype_formats`.
        dtype_formats : dict
            A `{dtype:str,}` dictionary that sets the default Excel format for the
            given dtype. (This can be overridden on a per-column basis by the
            `column_formats` param). It is also valid to use dtype groups such as
            `pl.FLOAT_DTYPES` as the dtype/format key, to simplify setting uniform
            integer and float formats.
        conditional_formats : dict
            A dictionary of colname (or selector) keys to a format str, dict, or list
            that defines conditional formatting options for the specified columns.

            * If supplying a string typename, should be one of the valid `xlsxwriter`
              types such as "3_color_scale", "data_bar", etc.
            * If supplying a dictionary you can make use of any/all `xlsxwriter`
              supported options, including icon sets, formulae, etc.
            * Supplying multiple columns as a tuple/key will apply a single format
              across all columns - this is effective in creating a heatmap, as the
              min/max values will be determined across the entire range, not per-column.
            * Finally, you can also supply a list made up from the above options
              in order to apply *more* than one conditional format to the same range.
        header_format : dict
            A `{key:value,}` dictionary of `xlsxwriter` format options to apply
            to the table header row, such as `{"bold":True, "font_color":"#702963"}`.
        column_totals : {bool, list, dict}
            Add a column-total row to the exported table.

            * If True, all numeric columns will have an associated total using "sum".
            * If passing a string, it must be one of the valid total function names
              and all numeric columns will have an associated total using that function.
            * If passing a list of colnames, only those given will have a total.
            * For more control, pass a `{colname:funcname,}` dict.

            Valid total function names are "average", "count_nums", "count", "max",
            "min", "std_dev", "sum", and "var".
        column_widths : {dict, int}
            A `{colname:int,}` or `{selector:int,}` dict or a single integer that
            sets (or overrides if autofitting) table column widths, in integer pixel
            units. If given as an integer the same value is used for all table columns.
        row_totals : {dict, bool}
            Add a row-total column to the right-hand side of the exported table.

            * If True, a column called "total" will be added at the end of the table
              that applies a "sum" function row-wise across all numeric columns.
            * If passing a list/sequence of column names, only the matching columns
              will participate in the sum.
            * Can also pass a `{colname:columns,}` dictionary to create one or
              more total columns with distinct names, referencing different columns.
        row_heights : {dict, int}
            An int or `{row_index:int,}` dictionary that sets the height of the given
            rows (if providing a dictionary) or all rows (if providing an integer) that
            intersect with the table body (including any header and total row) in
            integer pixel units. Note that `row_index` starts at zero and will be
            the header row (unless `include_header` is False).
        sparklines : dict
            A `{colname:list,}` or `{colname:dict,}` dictionary defining one or more
            sparklines to be written into a new column in the table.

            * If passing a list of colnames (used as the source of the sparkline data)
              the default sparkline settings are used (eg: line chart with no markers).
            * For more control an `xlsxwriter`-compliant options dict can be supplied,
              in which case three additional polars-specific keys are available:
              "columns", "insert_before", and "insert_after". These allow you to define
              the source columns and position the sparkline(s) with respect to other
              table columns. If no position directive is given, sparklines are added to
              the end of the table (eg: to the far right) in the order they are given.
        formulas : dict
            A `{colname:formula,}` or `{colname:dict,}` dictionary defining one or
            more formulas to be written into a new column in the table. Note that you
            are strongly advised to use structured references in your formulae wherever
            possible to make it simple to reference columns by name.

            * If providing a string formula (such as "=[@colx]*[@coly]") the column will
              be added to the end of the table (eg: to the far right), after any default
              sparklines and before any row_totals.
            * For the most control supply an options dictionary with the following keys:
              "formula" (mandatory), one of "insert_before" or "insert_after", and
              optionally "return_dtype". The latter is used to appropriately format the
              output of the formula and allow it to participate in row/column totals.
        float_precision : int
            Default number of decimals displayed for floating point columns (note that
            this is purely a formatting directive; the actual values are not rounded).
        include_header : bool
            Indicate if the table should be created with a header row.
        autofilter : bool
            If the table has headers, provide autofilter capability.
        autofit : bool
            Calculate individual column widths from the data.
        hidden_columns : list
             A list or selector representing table columns to hide in the worksheet.
        hide_gridlines : bool
            Do not display any gridlines on the output worksheet.
        sheet_zoom : int
            Set the default zoom level of the output worksheet.
        freeze_panes : str | (str, int, int) | (int, int) | (int, int, int, int)
            Freeze workbook panes.

            * If (row, col) is supplied, panes are split at the top-left corner of the
              specified cell, which are 0-indexed. Thus, to freeze only the top row,
              supply (1, 0).
            * Alternatively, cell notation can be used to supply the cell. For example,
              "A2" indicates the split occurs at the top-left of cell A2, which is the
              equivalent of (1, 0).
            * If (row, col, top_row, top_col) are supplied, the panes are split based on
              the `row` and `col`, and the scrolling region is inititalized to begin at
              the `top_row` and `top_col`. Thus, to freeze only the top row and have the
              scrolling region begin at row 10, column D (5th col), supply (1, 0, 9, 4).
              Using cell notation for (row, col), supplying ("A2", 9, 4) is equivalent.

        Notes
        -----
        * A list of compatible `xlsxwriter` format property names can be found here:
          https://xlsxwriter.readthedocs.io/format.html#format-methods-and-format-properties

        * Conditional formatting dictionaries should provide xlsxwriter-compatible
          definitions; polars will take care of how they are applied on the worksheet
          with respect to the relative sheet/column position. For supported options,
          see: https://xlsxwriter.readthedocs.io/working_with_conditional_formats.html

        * Similarly, sparkline option dictionaries should contain xlsxwriter-compatible
          key/values, as well as a mandatory polars "columns" key that defines the
          sparkline source data; these source columns should all be adjacent. Two other
          polars-specific keys are available to help define where the sparkline appears
          in the table: "insert_after", and "insert_before". The value associated with
          these keys should be the name of a column in the exported table.
          https://xlsxwriter.readthedocs.io/working_with_sparklines.html

        * Formula dictionaries *must* contain a key called "formula", and then optional
          "insert_after", "insert_before", and/or "return_dtype" keys. These additional
          keys allow the column to be injected into the table at a specific location,
          and/or to define the return type of the formula (eg: "Int64", "Float64", etc).
          Formulas that refer to table columns should use Excel's structured references
          syntax to ensure the formula is applied correctly and is table-relative.
          https://support.microsoft.com/en-us/office/using-structured-references-with-excel-tables-f5ed2452-2337-4f71-bed3-c8ae6d2b276e

        Examples
        --------
        Instantiate a basic DataFrame:

        >>> from random import uniform
        >>> from datetime import date
        >>>
        >>> df = pl.DataFrame(
        ...     {
        ...         "dtm": [date(2023, 1, 1), date(2023, 1, 2), date(2023, 1, 3)],
        ...         "num": [uniform(-500, 500), uniform(-500, 500), uniform(-500, 500)],
        ...         "val": [10_000, 20_000, 30_000],
        ...     }
        ... )

        Export to "dataframe.xlsx" (the default workbook name, if not specified) in the
        working directory, add column totals ("sum" by default) on all numeric columns,
        then autofit:

        >>> df.write_excel(column_totals=True, autofit=True)  # doctest: +SKIP

        Write frame to a specific location on the sheet, set a named table style,
        apply US-style date formatting, increase default float precision, apply a
        non-default total function to a single column, autofit:

        >>> df.write_excel(  # doctest: +SKIP
        ...     position="B4",
        ...     table_style="Table Style Light 16",
        ...     dtype_formats={pl.Date: "mm/dd/yyyy"},
        ...     column_totals={"num": "average"},
        ...     float_precision=6,
        ...     autofit=True,
        ... )

        Write the same frame to a named worksheet twice, applying different styles
        and conditional formatting to each table, adding table titles using explicit
        xlsxwriter integration:

        >>> from xlsxwriter import Workbook
        >>> with Workbook("multi_frame.xlsx") as wb:  # doctest: +SKIP
        ...     # basic/default conditional formatting
        ...     df.write_excel(
        ...         workbook=wb,
        ...         worksheet="data",
        ...         position=(3, 1),  # specify position as (row,col) coordinates
        ...         conditional_formats={"num": "3_color_scale", "val": "data_bar"},
        ...         table_style="Table Style Medium 4",
        ...     )
        ...
        ...     # advanced conditional formatting, custom styles
        ...     df.write_excel(
        ...         workbook=wb,
        ...         worksheet="data",
        ...         position=(len(df) + 7, 1),
        ...         table_style={
        ...             "style": "Table Style Light 4",
        ...             "first_column": True,
        ...         },
        ...         conditional_formats={
        ...             "num": {
        ...                 "type": "3_color_scale",
        ...                 "min_color": "#76933c",
        ...                 "mid_color": "#c4d79b",
        ...                 "max_color": "#ebf1de",
        ...             },
        ...             "val": {
        ...                 "type": "data_bar",
        ...                 "data_bar_2010": True,
        ...                 "bar_color": "#9bbb59",
        ...                 "bar_negative_color_same": True,
        ...                 "bar_negative_border_color_same": True,
        ...             },
        ...         },
        ...         column_formats={"num": "#,##0.000;[White]-#,##0.000"},
        ...         column_widths={"val": 125},
        ...         autofit=True,
        ...     )
        ...
        ...     # add some table titles (with a custom format)
        ...     ws = wb.get_worksheet_by_name("data")
        ...     fmt_title = wb.add_format(
        ...         {
        ...             "font_color": "#4f6228",
        ...             "font_size": 12,
        ...             "italic": True,
        ...             "bold": True,
        ...         }
        ...     )
        ...     ws.write(2, 1, "Basic/default conditional formatting", fmt_title)
        ...     ws.write(len(df) + 6, 1, "Customised conditional formatting", fmt_title)
        ...

        Export a table containing two different types of sparklines. Use default
        options for the "trend" sparkline and customised options (and positioning)
        for the "+/-" win_loss sparkline, with non-default integer dtype formatting,
        column totals, a subtle two-tone heatmap and hidden worksheet gridlines:

        >>> df = pl.DataFrame(
        ...     {
        ...         "id": ["aaa", "bbb", "ccc", "ddd", "eee"],
        ...         "q1": [100, 55, -20, 0, 35],
        ...         "q2": [30, -10, 15, 60, 20],
        ...         "q3": [-50, 0, 40, 80, 80],
        ...         "q4": [75, 55, 25, -10, -55],
        ...     }
        ... )
        >>> df.write_excel(  # doctest: +SKIP
        ...     table_style="Table Style Light 2",
        ...     # apply accounting format to all flavours of integer
        ...     dtype_formats={pl.INTEGER_DTYPES: "#,##0_);(#,##0)"},
        ...     sparklines={
        ...         # default options; just provide source cols
        ...         "trend": ["q1", "q2", "q3", "q4"],
        ...         # customised sparkline type, with positioning directive
        ...         "+/-": {
        ...             "columns": ["q1", "q2", "q3", "q4"],
        ...             "insert_after": "id",
        ...             "type": "win_loss",
        ...         },
        ...     },
        ...     conditional_formats={
        ...         # create a unified multi-column heatmap
        ...         ("q1", "q2", "q3", "q4"): {
        ...             "type": "2_color_scale",
        ...             "min_color": "#95b3d7",
        ...             "max_color": "#ffffff",
        ...         },
        ...     },
        ...     column_totals=["q1", "q2", "q3", "q4"],
        ...     row_totals=True,
        ...     hide_gridlines=True,
        ... )

        Export a table containing an Excel formula-based column that calculates a
        standardised Z-score, showing use of structured references in conjunction
        with positioning directives, column totals, and custom formatting.

        >>> df = pl.DataFrame(
        ...     {
        ...         "id": ["a123", "b345", "c567", "d789", "e101"],
        ...         "points": [99, 45, 50, 85, 35],
        ...     }
        ... )
        >>> df.write_excel(  # doctest: +SKIP
        ...     table_style={
        ...         "style": "Table Style Medium 15",
        ...         "first_column": True,
        ...     },
        ...     column_formats={
        ...         "id": {"font": "Consolas"},
        ...         "points": {"align": "center"},
        ...         "z-score": {"align": "center"},
        ...     },
        ...     column_totals="average",
        ...     formulas={
        ...         "z-score": {
        ...             # use structured references to refer to the table columns and 'totals' row
        ...             "formula": "=STANDARDIZE([@points], [[#Totals],[points]], STDEV([points]))",
        ...             "insert_after": "points",
        ...             "return_dtype": pl.Float64,
        ...         }
        ...     },
        ...     hide_gridlines=True,
        ...     sheet_zoom=125,
        ... )

        """  # noqa: W505
        try:
            import xlsxwriter
            from xlsxwriter.utility import xl_cell_to_rowcol
        except ImportError:
            raise ImportError(
                "Excel export requires xlsxwriter"
                "\n\nPlease run: pip install XlsxWriter"
            ) from None

        # setup workbook/worksheet
        wb, ws, can_close = _xl_setup_workbook(workbook, worksheet)
        df, is_empty = self, not len(self)

        # setup table format/columns
        fmt_cache = _XLFormatCache(wb)
        column_formats = column_formats or {}
        table_style, table_options = _xl_setup_table_options(table_style)
        table_name = table_name or _xl_unique_table_name(wb)
        table_columns, column_formats, df = _xl_setup_table_columns(  # type: ignore[assignment]
            df=df,
            format_cache=fmt_cache,
            column_formats=column_formats,
            column_totals=column_totals,
            dtype_formats=dtype_formats,
            header_format=header_format,
            float_precision=float_precision,
            row_totals=row_totals,
            sparklines=sparklines,
            formulas=formulas,
        )

        # normalise cell refs (eg: "B3" => (2,1)) and establish table start/finish,
        # accounting for potential presence/absence of headers and a totals row.
        table_start = (
            xl_cell_to_rowcol(position) if isinstance(position, str) else position
        )
        table_finish = (
            table_start[0]
            + len(df)
            + int(is_empty)
            - int(not include_header)
            + int(bool(column_totals)),
            table_start[1] + len(df.columns) - 1,
        )

        # write table structure and formats into the target sheet
        if not is_empty or include_header:
            ws.add_table(
                *table_start,
                *table_finish,
                {
                    "style": table_style,
                    "columns": table_columns,
                    "header_row": include_header,
                    "autofilter": autofilter,
                    "total_row": bool(column_totals) and not is_empty,
                    "name": table_name,
                    **table_options,
                },
            )

            # write data into the table range, column-wise
            if not is_empty:
                column_start = [table_start[0] + int(include_header), table_start[1]]
                for c in df.columns:
                    if c in self.columns:
                        ws.write_column(
                            *column_start,
                            data=df[c].to_list(),
                            cell_format=column_formats.get(c),
                        )
                    column_start[1] += 1

            # apply conditional formats
            if conditional_formats:
                _xl_apply_conditional_formats(
                    df=df,
                    ws=ws,
                    conditional_formats=conditional_formats,
                    table_start=table_start,
                    include_header=include_header,
                    format_cache=fmt_cache,
                )
        # additional column-level properties
        if hidden_columns is None:
            hidden_columns = ()
        hidden_columns = _expand_selectors(df, hidden_columns)
        if isinstance(column_widths, int):
            column_widths = {column: column_widths for column in df.columns}
        else:
            column_widths = _expand_selector_dicts(  # type: ignore[assignment]
                df, column_widths, expand_keys=True, expand_values=False
            )
        column_widths = _unpack_multi_column_dict(column_widths or {})  # type: ignore[assignment]

        for column in df.columns:
            col_idx, options = table_start[1] + df.get_column_index(column), {}
            if column in hidden_columns:
                options = {"hidden": True}
            if column in column_widths:  # type: ignore[operator]
                ws.set_column_pixels(
                    col_idx,
                    col_idx,
                    column_widths[column],  # type: ignore[index]
                    None,
                    options,
                )
            elif options:
                ws.set_column(col_idx, col_idx, None, None, options)

        # finally, inject any sparklines into the table
        for column, params in (sparklines or {}).items():
            _xl_inject_sparklines(
                ws,
                df,
                table_start,
                column,
                include_header=include_header,
                params=params,
            )

        # worksheet options
        if hide_gridlines:
            ws.hide_gridlines(2)
        if sheet_zoom:
            ws.set_zoom(sheet_zoom)
        if row_heights:
            if isinstance(row_heights, int):
                for idx in range(table_start[0], table_finish[0] + 1):
                    ws.set_row_pixels(idx, row_heights)
            elif isinstance(row_heights, dict):
                for idx, height in _unpack_multi_column_dict(row_heights).items():  # type: ignore[assignment]
                    ws.set_row_pixels(idx, height)

        # table/rows all written; apply (optional) autofit
        if autofit and not is_empty:
            xlv = xlsxwriter.__version__
            if parse_version(xlv) < (3, 0, 8):
                raise ModuleUpgradeRequired(
                    f"`autofit=True` requires xlsxwriter 3.0.8 or higher, found {xlv}"
                )
            ws.autofit()

        if freeze_panes:
            if isinstance(freeze_panes, str):
                ws.freeze_panes(freeze_panes)
            else:
                ws.freeze_panes(*freeze_panes)

        if can_close:
            wb.close()
        return wb
