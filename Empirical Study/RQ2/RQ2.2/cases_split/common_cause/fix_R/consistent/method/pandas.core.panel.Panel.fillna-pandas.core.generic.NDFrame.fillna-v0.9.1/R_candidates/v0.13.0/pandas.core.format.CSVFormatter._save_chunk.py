    def _save_chunk(self, start_i, end_i):

        data_index = self.data_index

        # create the data for a chunk
        slicer = slice(start_i, end_i)
        for i in range(len(self.blocks)):
            b = self.blocks[i]
            d = b.to_native_types(slicer=slicer, na_rep=self.na_rep,
                                  float_format=self.float_format,
                                  date_format=self.date_format)

            for i, item in enumerate(b.items):

                # self.data is a preallocated list
                self.data[self.column_map[b][i]] = d[i]

        ix = data_index.to_native_types(slicer=slicer, na_rep=self.na_rep,
                                        float_format=self.float_format,
                                        date_format=self.date_format)

        lib.write_csv_rows(self.data, ix, self.nlevels, self.cols, self.writer)
