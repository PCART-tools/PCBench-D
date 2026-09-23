    @doc(storage_options=generic._shared_docs["storage_options"])
    def write(
        self,
        writer,
        sheet_name="Sheet1",
        startrow=0,
        startcol=0,
        freeze_panes=None,
        engine=None,
        storage_options: StorageOptions = None,
    ):
        """
        writer : path-like, file-like, or ExcelWriter object
            File path or existing ExcelWriter
        sheet_name : str, default 'Sheet1'
            Name of sheet which will contain DataFrame
        startrow :
            upper left cell row to dump data frame
        startcol :
            upper left cell column to dump data frame
        freeze_panes : tuple of integer (length 2), default None
            Specifies the one-based bottommost row and rightmost column that
            is to be frozen
        engine : string, default None
            write engine to use if writer is a path - you can also set this
            via the options ``io.excel.xlsx.writer``, ``io.excel.xls.writer``,
            and ``io.excel.xlsm.writer``.

            .. deprecated:: 1.2.0

                As the `xlwt <https://pypi.org/project/xlwt/>`__ package is no longer
                maintained, the ``xlwt`` engine will be removed in a future
                version of pandas.

        {storage_options}

            .. versionadded:: 1.2.0
        """
        from pandas.io.excel import ExcelWriter

        num_rows, num_cols = self.df.shape
        if num_rows > self.max_rows or num_cols > self.max_cols:
            raise ValueError(
                f"This sheet is too large! Your sheet size is: {num_rows}, {num_cols} "
                f"Max sheet size is: {self.max_rows}, {self.max_cols}"
            )

        formatted_cells = self.get_formatted_cells()
        if isinstance(writer, ExcelWriter):
            need_save = False
        else:
            # error: Cannot instantiate abstract class 'ExcelWriter' with abstract
            # attributes 'engine', 'save', 'supported_extensions' and 'write_cells'
            writer = ExcelWriter(  # type: ignore[abstract]
                writer, engine=engine, storage_options=storage_options
            )
            need_save = True

        try:
            writer.write_cells(
                formatted_cells,
                sheet_name,
                startrow=startrow,
                startcol=startcol,
                freeze_panes=freeze_panes,
            )
        finally:
            # make sure to close opened file handles
            if need_save:
                writer.close()
