    @Appender(_shared_docs['to_excel'] % _shared_doc_kwargs)
    def to_excel(self, excel_writer, sheet_name='Sheet1', na_rep='',
                 float_format=None, columns=None, header=True, index=True,
                 index_label=None, startrow=0, startcol=0, engine=None,
                 merge_cells=True, encoding=None, inf_rep='inf', verbose=True,
                 freeze_panes=None):

        from pandas.io.formats.excel import ExcelFormatter
        formatter = ExcelFormatter(self, na_rep=na_rep, cols=columns,
                                   header=header,
                                   float_format=float_format, index=index,
                                   index_label=index_label,
                                   merge_cells=merge_cells,
                                   inf_rep=inf_rep)
        formatter.write(excel_writer, sheet_name=sheet_name, startrow=startrow,
                        startcol=startcol, freeze_panes=freeze_panes,
                        engine=engine)
