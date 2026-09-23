    def _write_header(self, indent):
        if not self.fmt.header:
            # write nothing
            return indent

        def _column_header():
            if self.fmt.index:
                row = [''] * (self.frame.index.nlevels - 1)
            else:
                row = []

            if isinstance(self.columns, MultiIndex):
                if self.fmt.has_column_names and self.fmt.index:
                    row.append(single_column_table(self.columns.names))
                else:
                    row.append('')
                style = "text-align: %s;" % self.fmt.justify
                row.extend([single_column_table(c, self.fmt.justify, style) for
                            c in self.columns])
            else:
                if self.fmt.index:
                    row.append(self.columns.name or '')
                row.extend(self.columns[:self.max_cols])
                if len(self.columns) > self.max_cols:
                    row.append('')
            return row

        self.write('<thead>', indent)
        row = []

        indent += self.indent_delta

        if isinstance(self.columns, MultiIndex):
            template = 'colspan="%d" halign="left"'

            # GH3547
            sentinel = com.sentinel_factory()
            levels = self.columns.format(sparsify=sentinel, adjoin=False,
                                         names=False)
            # Truncate column names
            if len(levels[0]) > self.max_cols:
                levels = [lev[:self.max_cols] for lev in levels]
                truncated = True
            else:
                truncated = False

            level_lengths = _get_level_lengths(levels, sentinel)

            row_levels = self.frame.index.nlevels

            for lnum, (records, values) in enumerate(zip(level_lengths,
                                                         levels)):
                name = self.columns.names[lnum]
                row = [''] * (row_levels - 1) + ['' if name is None
                                                 else str(name)]

                tags = {}
                j = len(row)
                for i, v in enumerate(values):
                    if i in records:
                        if records[i] > 1:
                            tags[j] = template % records[i]
                    else:
                        continue
                    j += 1
                    row.append(v)

                if truncated:
                    row.append('')

                self.write_tr(row, indent, self.indent_delta, tags=tags,
                              header=True)
        else:
            col_row = _column_header()
            align = self.fmt.justify

            self.write_tr(col_row, indent, self.indent_delta, header=True,
                          align=align)

        if self.fmt.has_index_names:
            row = [
                x if x is not None else '' for x in self.frame.index.names
            ] + [''] * min(len(self.columns), self.max_cols)
            self.write_tr(row, indent, self.indent_delta, header=True)

        indent -= self.indent_delta
        self.write('</thead>', indent)

        return indent
