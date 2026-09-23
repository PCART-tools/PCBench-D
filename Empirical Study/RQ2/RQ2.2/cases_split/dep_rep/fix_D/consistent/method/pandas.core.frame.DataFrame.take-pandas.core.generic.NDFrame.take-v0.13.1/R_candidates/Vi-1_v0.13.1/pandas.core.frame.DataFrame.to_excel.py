    def to_excel(self, excel_writer, sheet_name='Sheet1', na_rep='',
                 float_format=None, cols=None, header=True, index=True,
                 index_label=None, startrow=0, startcol=0, engine=None,
                 merge_cells=True):
        """
        Write DataFrame to a excel sheet

        Parameters
        ----------
        excel_writer : string or ExcelWriter object
            File path or existing ExcelWriter
        sheet_name : string, default 'Sheet1'
            Name of sheet which will contain DataFrame
        na_rep : string, default ''
            Missing data representation
        float_format : string, default None
            Format string for floating point numbers
        cols : sequence, optional
            Columns to write
        header : boolean or list of string, default True
            Write out column names. If a list of string is given it is
            assumed to be aliases for the column names
        index : boolean, default True
            Write row names (index)
        index_label : string or sequence, default None
            Column label for index column(s) if desired. If None is given, and
            `header` and `index` are True, then the index names are used. A
            sequence should be given if the DataFrame uses MultiIndex.
        startow :
            upper left cell row to dump data frame
        startcol :
            upper left cell column to dump data frame
        engine : string, default None
            write engine to use - you can also set this via the options
            ``io.excel.xlsx.writer``, ``io.excel.xls.writer``, and
            ``io.excel.xlsm.writer``.
        merge_cells : boolean, default True
            Write MultiIndex and Hierarchical Rows as merged cells.

        Notes
        -----
        If passing an existing ExcelWriter object, then the sheet will be added
        to the existing workbook.  This can be used to save different
        DataFrames to one workbook:

        >>> writer = ExcelWriter('output.xlsx')
        >>> df1.to_excel(writer,'Sheet1')
        >>> df2.to_excel(writer,'Sheet2')
        >>> writer.save()
        """
        from pandas.io.excel import ExcelWriter
        need_save = False
        if isinstance(excel_writer, compat.string_types):
            excel_writer = ExcelWriter(excel_writer, engine=engine)
            need_save = True

        formatter = fmt.ExcelFormatter(self,
                                       na_rep=na_rep,
                                       cols=cols,
                                       header=header,
                                       float_format=float_format,
                                       index=index,
                                       index_label=index_label,
                                       merge_cells=merge_cells)
        formatted_cells = formatter.get_formatted_cells()
        excel_writer.write_cells(formatted_cells, sheet_name,
                                 startrow=startrow, startcol=startcol)
        if need_save:
            excel_writer.save()
