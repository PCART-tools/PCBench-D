    def _save_chunk(self, start_i: int, end_i: int) -> None:
        # create the data for a chunk
        slicer = slice(start_i, end_i)
        df = self.obj.iloc[slicer]

        res = df._mgr.to_native_types(**self._number_format)
        data = [res.iget_values(i) for i in range(len(res.items))]

        ix = self.data_index[slicer]._format_native_types(**self._number_format)
        libwriters.write_csv_rows(
            data,
            ix,
            self.nlevels,
            self.cols,
            self.writer,
        )
