    @Appender(generic._shared_docs['to_excel'] % _shared_doc_kwargs)
    def to_excel(self, excel_writer, sheet_name='Sheet1', na_rep='',
                 float_format=None, columns=None, header=True, index=True,
                 index_label=None, startrow=0, startcol=0, engine=None,
                 merge_cells=True, encoding=None, inf_rep='inf', verbose=True):
        df = self.to_frame()
        df.to_excel(excel_writer=excel_writer, sheet_name=sheet_name,
                    na_rep=na_rep, float_format=float_format, columns=columns,
                    header=header, index=index, index_label=index_label,
                    startrow=startrow, startcol=startcol, engine=engine,
                    merge_cells=merge_cells, encoding=encoding,
                    inf_rep=inf_rep, verbose=verbose)
