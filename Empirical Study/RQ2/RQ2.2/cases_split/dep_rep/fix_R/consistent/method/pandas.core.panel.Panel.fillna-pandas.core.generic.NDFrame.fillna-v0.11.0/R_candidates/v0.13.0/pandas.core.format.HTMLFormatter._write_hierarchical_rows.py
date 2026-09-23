    def _write_hierarchical_rows(self, fmt_values, indent):
        template = 'rowspan="%d" valign="top"'

        frame = self.frame
        ncols = min(len(self.columns), self.max_cols)
        nrows = min(len(self.frame), self.max_rows)

        truncate = (len(frame) > self.max_rows)

        idx_values = frame.index[:nrows].format(sparsify=False, adjoin=False,
                                                names=False)
        idx_values = lzip(*idx_values)

        if self.fmt.sparsify:

            # GH3547
            sentinel = com.sentinel_factory()
            levels = frame.index[:nrows].format(sparsify=sentinel,
                                                adjoin=False, names=False)
            # Truncate row names
            if truncate:
                levels = [lev[:self.max_rows] for lev in levels]

            level_lengths = _get_level_lengths(levels, sentinel)

            for i in range(min(len(frame), self.max_rows)):
                row = []
                tags = {}

                sparse_offset = 0
                j = 0
                for records, v in zip(level_lengths, idx_values[i]):
                    if i in records:
                        if records[i] > 1:
                            tags[j] = template % records[i]
                    else:
                        sparse_offset += 1
                        continue

                    j += 1
                    row.append(v)

                row.extend(fmt_values[j][i] for j in range(ncols))
                self.write_tr(row, indent, self.indent_delta, tags=tags,
                              nindex_levels=len(levels) - sparse_offset)
        else:
            for i in range(len(frame)):
                idx_values = list(zip(*frame.index.format(sparsify=False,
                                                          adjoin=False,
                                                          names=False)))
                row = []
                row.extend(idx_values[i])
                row.extend(fmt_values[j][i] for j in range(ncols))
                self.write_tr(row, indent, self.indent_delta, tags=None,
                              nindex_levels=frame.index.nlevels)

        # Truncation markers (...)
        if truncate:
            row = ([''] * frame.index.nlevels) + (['...'] * ncols)
            self.write_tr(row, indent, self.indent_delta, tags=None)
