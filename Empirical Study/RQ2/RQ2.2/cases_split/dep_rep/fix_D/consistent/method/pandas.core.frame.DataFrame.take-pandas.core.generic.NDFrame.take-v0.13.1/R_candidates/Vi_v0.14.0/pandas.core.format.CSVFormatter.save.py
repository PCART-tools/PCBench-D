    def save(self):
        # create the writer & save
        if hasattr(self.path_or_buf, 'write'):
            f = self.path_or_buf
            close = False
        else:
            f = com._get_handle(self.path_or_buf, self.mode,
                                encoding=self.encoding)
            close = True

        try:
            writer_kwargs = dict(lineterminator=self.line_terminator,
                                 delimiter=self.sep, quoting=self.quoting,
                                 doublequote=self.doublequote,
                                 escapechar=self.escapechar,
                                 quotechar=self.quotechar)
            if self.encoding is not None:
                writer_kwargs['encoding'] = self.encoding
                self.writer = com.UnicodeWriter(f, **writer_kwargs)
            else:
                self.writer = csv.writer(f, **writer_kwargs)

            if self.engine == 'python':
            # to be removed in 0.13
                self._helper_csv(self.writer, na_rep=self.na_rep,
                                 float_format=self.float_format,
                                 cols=self.cols, header=self.header,
                                 index=self.index,
                                 index_label=self.index_label,
                                 date_format=self.date_format)

            else:
                self._save()

        finally:
            if close:
                f.close()
