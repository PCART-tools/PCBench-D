    def _write_header(self, indent):
        truncate_h = self.fmt.truncate_h
        row_levels = self.frame.index.nlevels
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
                row.extend(self.columns)
            return row

        self.write('<thead>', indent)
        row = []

        indent += self.indent_delta

        if isinstance(self.columns, MultiIndex):
            template = 'colspan="%d" halign="left"'

            if self.fmt.sparsify:
                # GH3547
                sentinel = com.sentinel_factory()
            else:
                sentinel = None
            levels = self.columns.format(sparsify=sentinel,
                                         adjoin=False, names=False)
            level_lengths = _get_level_lengths(levels, sentinel)
            inner_lvl = len(level_lengths) - 1
            for lnum, (records, values) in enumerate(zip(level_lengths,
                                                         levels)):
                if truncate_h:
                    # modify the header lines
                    ins_col = self.fmt.tr_col_num
                    if self.fmt.sparsify:
                        recs_new = {}
                        # Increment tags after ... col.
                        for tag, span in list(records.items()):
                            if tag >= ins_col:
                                recs_new[tag + 1] = span
                            elif tag + span > ins_col:
                                recs_new[tag] = span + 1
                                if lnum == inner_lvl:
                                    values = values[:ins_col] + (u('...'),) + \
                                        values[ins_col:]
                                else:  # sparse col headers do not receive a ...
                                    values = (values[:ins_col] + (values[ins_col - 1],) +
                                              values[ins_col:])
                            else:
                                recs_new[tag] = span
                            # if ins_col lies between tags, all col headers get ...
                            if tag + span == ins_col:
                                recs_new[ins_col] = 1
                                values = values[:ins_col] + (u('...'),) + \
                                    values[ins_col:]
                        records = recs_new
                        inner_lvl = len(level_lengths) - 1
                        if lnum == inner_lvl:
                            records[ins_col] = 1
                    else:
                        recs_new = {}
                        for tag, span in list(records.items()):
                            if tag >= ins_col:
                                recs_new[tag + 1] = span
                            else:
                                recs_new[tag] = span
                        recs_new[ins_col] = 1
                        records = recs_new
                        values = values[:ins_col] + [u('...')] + values[ins_col:]

                name = self.columns.names[lnum]
                row = [''] * (row_levels - 1) + ['' if name is None
                                                 else com.pprint_thing(name)]

                if row == [""] and self.fmt.index is False:
                    row = []

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
                self.write_tr(row, indent, self.indent_delta, tags=tags,
                              header=True)
        else:
            col_row = _column_header()
            align = self.fmt.justify

            if truncate_h:
                ins_col = row_levels + self.fmt.tr_col_num
                col_row.insert(ins_col, '...')

            self.write_tr(col_row, indent, self.indent_delta, header=True,
                          align=align)

        if self.fmt.has_index_names:
            row = [
                x if x is not None else '' for x in self.frame.index.names
            ] + [''] * min(len(self.columns), self.max_cols)
            if truncate_h:
                ins_col = row_levels + self.fmt.tr_col_num
                row.insert(ins_col, '')
            self.write_tr(row, indent, self.indent_delta, header=True)

        indent -= self.indent_delta
        self.write('</thead>', indent)

        return indent
